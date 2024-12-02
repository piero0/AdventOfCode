import Data.Ix (inRange)

lineToList l = map (read :: String -> Int) $ words l

dataToIntList x = map lineToList $ lines x

parseLevel l = zipWith (\x y -> y - x) l $ tail l

isMono l
  | elem 0 l = False
  | all (> 0) l = True
  | all (< 0) l = True
  | otherwise = False

checkInRange l = all (inRange (1, 3) . abs) l

isSafe :: [Int] -> Bool
isSafe x = isMono x && checkInRange x

isSafeWithoutOne :: [Int] -> Bool
isSafeWithoutOne l =
  let idx = take (length l) [0 ..]
      skipOne (a, b) = a ++ tail b
      allOneLess = map (\s -> skipOne $ splitAt s l) idx
      results = map (isSafe . parseLevel) allOneLess
   in any id results

main = do
  content <- readFile "input"
  let levels = dataToIntList content
  let safes = map isSafeWithoutOne levels
  let len = length $ filter id safes
  print len
