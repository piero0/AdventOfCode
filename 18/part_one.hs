import Data.Map.Strict qualified as M
import Data.Set qualified as S
import Debug.Trace (trace)
import System.Environment (getArgs)

maxy = 71

dest = maxy - 1

elms = 1024

-- maxy = 7
-- dest = maxy - 1
-- elms = 12

parseInput i = map ((\(a, b) -> ((read :: String -> Int) a, (read :: String -> Int) $ tail b)) . break (== ',')) $ lines i

getNeigh :: (Int, Int) -> [(Int, Int)] -> S.Set (Int, Int) -> [(Int, Int)]
getNeigh c obst vis =
  let np a b = (fst a + fst b, snd a + snd b)
      inGrid (x, y) = x >= 0 && x < maxy && y >= 0 && y < maxy
      isObs x = x `elem` obst
      checkN np = if not (inGrid np) || isObs np || S.member np vis then (-1, -1) else np
   in filter (\a -> a /= (-1, -1)) $ map (checkN . np c) [(0, 1), (1, 0), (-1, 0), (0, -1)]

doBfs :: M.Map (Int, Int) Int -> [(Int, Int)] -> [(Int, Int)] -> S.Set (Int, Int) -> Int
doBfs d obs path vis
  -- \| d == 1 = -2
  | null path = -1
  | cur == (dest, dest) = curd
  | otherwise = doBfs upD obs newpath visited
  where
    -- trace ("c " ++ show cur ++ "p " ++ show path ++ " np " ++ show newpath)

    cur = head path
    curd = d M.! cur
    visited = S.insert cur vis
    neigh = if S.member cur vis then [] else getNeigh cur obs visited
    upD = foldl (\d a -> M.insert a (curd + 1) d) d neigh
    newpath = drop 1 path ++ neigh

main = do
  cnt <- getArgs >>= readFile . head
  let obs = take elms $ parseInput cnt
  print obs
  let res = doBfs (M.insert (0, 0) 0 M.empty) obs [(0, 0)] S.empty
  print res
