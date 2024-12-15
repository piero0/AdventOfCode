{-# OPTIONS_GHC -Wno-unrecognised-pragmas #-}

{-# HLINT ignore "Eta reduce" #-}

import Data.Map.Strict qualified as M
import Data.Text qualified as T

parseData l =
  let a = T.splitOn (T.pack " ") l
      b = map (T.drop 2) a
      c = map (T.splitOn (T.pack ",")) b
   in map (map ((read :: String -> Int) . T.unpack)) c

-- excercise - create splitOn for lists

solve i (mx, my) l =
  let s = head l
      v = last l
      x = (head s + i * head v) `mod` mx
      y = (last s + i * last v) `mod` my
   in (abs x, abs y)

lengths g = M.foldl max 0 pm
  where
    pm = ptsToMap g M.empty

findTree maxy a i =
  lengths $ map (solve i maxy) a

ptsToMap pts pm = foldl (\m x -> M.insertWith (+) (snd x) 1 m) pm pts

main = do
  d <- readFile "../data/2024/14/input"
  let lns = T.lines (T.pack d)
  let a = map parseData lns
  -- let maxy = (11, 7)
  let maxy = (101, 103)

  -- let r1 = map (solve 1 maxy) a
  -- print $ ptsToMap r1 M.empty
  -- let r = lengths r1
  let r = map (findTree maxy a) [1 .. 10000]
  -- print r
  let m = foldl (\b n -> if snd n > snd b then n else b) (0, 0) $ zip [1 ..] r
  print m
