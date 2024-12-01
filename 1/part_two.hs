import Data.List
import Data.Map qualified as Map
import System.IO

getMap = foldr (\l -> Map.insertWith (+) l 1) Map.empty

main = do
  content <- readFile "input"

  let twoLists = transpose $ map words $ lines content
  let nums = map (map (read :: String -> Int)) twoLists

  let entA = getMap (head nums)
  let entB = getMap (last nums)

  let totalSum = sum $ Map.mapWithKey (\k v -> k * v * Map.findWithDefault 0 k entB) entA
  print totalSum
