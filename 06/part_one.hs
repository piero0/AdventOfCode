import Data.List
import Data.List.Split
import System.Environment

combine :: [String] -> Int
combine nums =
  let ns = map read $ init nums
      ops = last nums
      op = if ops == "*" then (*) else (+)
   in foldl1 op ns

main = do
  raw <- getArgs >>= readFile . head
  let nums = transpose $ map (filter (/= "") . splitOn " ") $ lines raw
  let res = sum $ map combine nums
  print res
