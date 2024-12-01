import Data.List
import System.IO

main = do
  content <- readFile "input"
  -- split into two lists
  let twoLists = transpose $ map words $ lines content
  let nums = map (map (read :: String -> Int)) twoLists
  let sorted = transpose $ map sort nums
  let result = sum $ map (abs . foldr (-) 0) sorted
  print result
