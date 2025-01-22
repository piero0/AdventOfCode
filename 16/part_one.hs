import Data.Array qualified as Ar
import Data.List (foldl')
import Data.Map.Strict qualified as M
import Data.Set qualified as S
import System.Environment

data Dir = N | E | S | W deriving (Show, Eq)

type Pt = (Int, Int)

type DPt = (Pt, Dir)

type Maze = Ar.Array Pt Char

type DistMap = M.Map DPt Int

mazeToArray :: [String] -> Maze
mazeToArray r =
  let w = length (head r) - 1
      h = length r - 1
      convertRow :: Int -> String -> [((Int, Int), Char)]
      convertRow rowNum = zipWith (\x c -> ((rowNum, x), c)) [0 ..]
   in Ar.array ((0, 0), (h, w)) $ concat $ zipWith convertRow [0 ..] r

findPoint x maze = fst . head $ filter (\(_, c) -> c == x) $ Ar.assocs maze

-- initDistMap maze = foldl' (\m (p, c) -> getDist p c m) M.empty $ Ar.assocs maze
--   where
--     getDist p c m
--       | c == 'S' = M.insert p 0 m
--       | c == '.' = M.insert p (maxBound :: Int) m
--       | otherwise = m

findPath :: S.Set (Int, Pt) -> DistMap -> Maze -> DistMap
findPath !toVis !dists maze
  | S.null toVis = dists
  | otherwise =
      let (newVis, newDist) = nextStep toVis dists maze
       in findPath newVis newDist maze
  where
    nextStep !toVis !dist maze = undefined

main = do
  raw <- getArgs >>= readFile . head
  let maze = mazeToArray $ lines raw
  let start = findPoint 'S' maze
  let target = findPoint 'E' maze
  let toVisit = S.singleton (0, start)
  let dists = M.singleton (start, S) 0
  let cost = findPath toVisit dists maze
  print dists
