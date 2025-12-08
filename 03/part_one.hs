{-# OPTIONS_GHC -Wno-x-partial #-}

import Data.Char
import Data.List
import Data.Maybe
import System.Environment

findN :: Int -> String -> Int
findN 0 nums = length nums
findN n nums
  | isNothing pos = findN (n - 1) nums
  | otherwise = fromJust pos
  where
    pos = elemIndex (intToDigit n) nums

getN :: String -> Int
getN nums =
  let f = findN 9 $ init nums
      nums2 = drop (f + 1) nums
      s = findN 9 nums2
   in read [nums !! f, nums2 !! s]

main = do
  txt <- getArgs >>= readFile . head
  print $ sum $ map getN $ lines txt
