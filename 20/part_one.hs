import Data.Array.IArray (Array, array, bounds, inRange, indices, (!))
import Data.List (sort)
import Data.Map qualified as M
import Data.Maybe (fromJust)
import Data.Set qualified as S
import Data.Tree (flatten)
import System.Environment (getArgs)

type Pt = (Int, Int)

type Maze = Array Pt Char

type MazeI = Array Pt Int

type DistM = M.Map Pt Int

makeAr :: [String] -> Maze
makeAr raw =
  let h = length raw - 1
      w = length (head raw) - 1
      row y r = zipWith (\x c -> ((x, y), c)) [0 ..] r
   in array ((0, 0), (w, h)) $ foldl (\acc (y, r) -> acc ++ row y r) [] $ zip [0 ..] raw

plus1 = [(1, 0), (0, 1), (-1, 0), (0, -1)]

plus2 = [(2, 0), (0, 2), (-2, 0), (0, -2)]

getN :: Pt -> Maze -> S.Set Pt -> [Pt] -> [Pt]
getN c arr vis dts = filter validN $ map (\d -> (fst c + fst d, snd c + snd d)) dts
  where
    inMaze p = inRange (bounds arr) p
    isDot p = (arr ! p) /= '#'
    validN n = not (S.member n vis) && inMaze n && isDot n

dfs :: Pt -> Maze -> S.Set Pt -> M.Map Pt Int -> M.Map Pt Int
dfs c arr vis dist
  | cc == 'E' = dist
  | otherwise = dfs nextP arr (S.insert c vis) (updateDist nextP dist)
  where
    cc = arr ! c
    nextP = head $ getN c arr vis plus1
    updateDist np dst = M.insert np (dst M.! c + 1) dst

distToArr :: DistM -> Maze -> MazeI
distToArr d arr = array (bounds arr) [(i, getPt i) | i <- indices arr]
  where
    getPt i = let dst = d M.! i in if arr ! i /= '#' then dst else -1

findShortcuts :: [(Pt, Int)] -> Maze -> MazeI -> [Int]
findShortcuts path arr dist = concatMap calcDist path
  where
    calcDist (p, d) = filter (>= 100) $ map (getDist d) $ getN p arr S.empty plus2
    getDist d np = (dist ! np) - d - 2

main = do
  raw <- getArgs >>= readFile . head
  let a = makeAr $ lines raw
  let s = fromJust $ lookup 'S' [(a ! i, i) | i <- indices a]
  -- print a
  -- print s
  let d = dfs s a S.empty (M.insert s 0 M.empty)
  -- print d
  let sc = findShortcuts (M.toList d) a (distToArr d a)
  print $ length sc
