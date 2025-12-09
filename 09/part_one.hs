{-# OPTIONS_GHC -Wno-x-partial #-}

import Data.List.Split
import System.Environment

type Pair = (Int, Int)

toPair :: String -> Pair
toPair txt =
  let fromList [x, y] = (read x, read y)
   in fromList $ splitOn "," txt

area (x, y) (w, z) = abs ((w - x) + 1) * abs ((z - y) + 1)

main = do
  txt <- getArgs >>= readFile . head
  let pairs = map toPair $ lines txt
  let allcomb = [(x, y) | x <- pairs, y <- pairs, x /= y]
  print $ maximum $ map (uncurry area) allcomb
