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

part1 obs elms = doBfs (M.insert (0, 0) 0 M.empty) (take elms obs) [(0, 0)] S.empty

part2 obs = until ((== -1) . fst) (takeMore obs) (0, elms)
  where
    takeMore obs (ret, el) = (part1 obs el, el + 1)

main = do
  cnt <- getArgs >>= readFile . head
  let obs = parseInput cnt
  let p1 = part1 obs elms
  print p1
  let p2 = part2 obs
  print p2
  print $ obs !! (snd p2 - 2)
