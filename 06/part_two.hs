import Data.List
import Data.List.Split
import Data.Maybe
import System.Environment
import Text.Read

combine :: (String, [Int]) -> Int
combine (ops, ns) =
  let op = if ops == "*" then (*) else (+)
   in foldl1 op ns

makeparts :: [Maybe Int] -> [[Int]]
makeparts [] = []
makeparts nums =
  let part = map fromJust $ takeWhile (/= Nothing) nums
      rems = drop (length part + 1) nums
   in part : makeparts rems

main = do
  raw <- getArgs >>= readFile . head
  let nums = map readMaybe $ transpose $ init $ lines raw
  let ops = filter (/= "") . splitOn " " $ last $ lines raw
  let inp = zip ops $ makeparts nums
  print $ sum $ map combine inp
