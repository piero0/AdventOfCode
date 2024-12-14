{-# OPTIONS_GHC -Wno-unrecognised-pragmas #-}

{-# HLINT ignore "Eta reduce" #-}
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

getQuadrant elms (qx, qy) =
  map (\(x, y) -> qy y && qx x) elms

getNum x = length $ filter id x

main = do
  d <- readFile "../data/2024/14/input"
  let lns = T.lines (T.pack d)
  let a = map parseData lns
  -- let maxy = (11, 7)
  let maxy = (101, 103)
  let o = map (solve 100 maxy) a
  let mx :: Int = fst maxy `div` 2
  let my :: Int = snd maxy `div` 2
  let qd = [((< mx), (< my)), ((> mx), (< my)), ((< mx), (> my)), ((> mx), (> my))]
  let r = product $ map (getNum . getQuadrant o) qd
  print r
