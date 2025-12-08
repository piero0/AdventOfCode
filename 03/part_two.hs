{-# OPTIONS_GHC -Wno-x-partial #-}

import Data.Char
import Data.List
import Data.Maybe
import System.Environment

findN :: Int -> Int -> String -> Int
findN 0 p nums = length nums
findN n p nums
  | isNothing pos || fromJust pos > limit = findN (n - 1) p nums
  | otherwise = fromJust pos
  where
    pos = elemIndex (intToDigit n) nums
    limit = length nums - p

getN 0 nums = []
getN p nums =
  let idx = findN 9 p nums
      newnums = drop (idx + 1) nums
   in nums !! idx : getN (p - 1) newnums

main = do
  txt <- getArgs >>= readFile . head
  let nums = map (getN 12) $ lines txt
  print $ sum $ map read nums
