import Debug.Trace

convertEntry (d : v) =
  let i = (read v :: Int)
   in if d == 'L' then -i else i

newElem prev next =
  let nval = prev + (next `mod` (signum next * 100))
      nval2 = if nval < 0 then 100 + nval else nval `mod` 100
      r = if nval < 0 then nval < 0 && prev /= 0 else nval >= 100
      rn = if r then 1 else 0
      num = next `div` (signum next * 100)
   in -- in trace ("prev " ++ show prev ++ " nval " ++ show nval ++ " nval2 " ++ show nval2 ++ " rn " ++ show rn ++ " num " ++ show num) (nval2, num + rn)
      (nval2, num + rn)

spinLock :: (Int, Int) -> [Int] -> [(Int, Int)]
-- spinLock prev [] = [prev]
-- spinLock prev (s : spins) = prev : spinLock (newElem (fst prev) s) spins

spinLock prev [] = []
spinLock prev (s : spins) = next : spinLock next spins
  where
    next = newElem (fst prev) s

makesum elems = sum (map snd elems)

main = do
  filedata <- readFile "input"
  let step1 = map convertEntry $ lines filedata
  print step1
  let step2 = spinLock (50, 0) step1
  print step2
  let step3 = makesum step2
  print step3
  let step4 = length $ filter (\(x, y) -> x == 0 && y == 0) step2
  print step4
  print (step3 + step4)
