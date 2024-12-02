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

main = do
  content <- readFile "input"
  let levels = dataToIntList content

  let rows = map parseLevel levels
  let safes = map (\x -> isMono x && checkInRange x) rows
  let len = length $ filter id safes
  print len
