import System.Environment

getValues :: Int -> [String] -> [Int]
getValues size text = map read vals
  where
    vals = drop (size + 1) text

splitText :: String -> (Int, Int)
splitText text =
  let minp = takeWhile (/= '-') text
      maxp = drop (length minp + 1) text
   in (read minp, read maxp)

getRanges :: [String] -> [(Int, Int)]
getRanges text = map splitText $ takeWhile (/= "") text

countRanges :: [(Int, Int)] -> Int -> Int
countRanges ranges val = length $ filter (inRange val) ranges
  where
    inRange val (a, b) = a <= val && b >= val

main = do
  raw <- getArgs >>= readFile . head
  let lns = lines raw
  let ranges = getRanges lns
  let vals = getValues (length ranges) lns
  let result = map (countRanges ranges) vals
  let answer = length $ filter (/= 0) result
  print answer
