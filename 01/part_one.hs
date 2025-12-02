convertEntry (d : v) =
  let i = (read v :: Int) `mod` 100
   in if d == 'L' then -i else i

newElem prev new
  | np < 0 = 100 + np
  | np >= 100 = np `mod` 100
  | otherwise = np
  where
    np = prev + new

spinLock :: Int -> [Int] -> [Int]
spinLock prev [] = []
spinLock prev (s : spins) = prev : spinLock (newElem prev s) spins

main = do
  filedata <- readFile "input"
  let step1 = map convertEntry $ lines filedata
  let step2 = spinLock 50 step1
  let step3 = length $ filter (== 0) step2
  print step3
