import Data.Bits (xor, (.&.), (.|.))
import Data.Char (digitToInt)
import Data.Map.Strict qualified as M
import Data.Set qualified as S
import System.Environment (getArgs)

getInputs inps = map convert inps
  where
    convert p = (take 3 p, digitToInt $ last p)

data Gate = Gate {op :: Op, x :: String, y :: String, z :: String} deriving (Show, Eq)

data Op = AND | OR | XOR deriving (Show, Eq)

createGate str gate =
  let x = take 3 str
      t = filter (/= ' ') $ take 3 $ drop 4 str
      y = filter (/= ' ') $ take 4 $ drop 7 str
      z = filter (/= ' ') $ drop 14 str
   in case t of
        "AND" -> Gate {op = AND, x = x, y = y, z = z}
        "OR" -> Gate {op = OR, x = x, y = y, z = z}
        "XOR" -> Gate {op = XOR, x = x, y = y, z = z}
        _ -> error "not happening"

getVal :: Gate -> M.Map String Int -> Int
getVal g m
  | op g == AND = getI (x g) .&. (getI (y g))
  | op g == OR = getI (x g) .|. (getI (y g))
  | op g == XOR = getI (x g) `xor` (getI (y g))
  | otherwise = error "wrong op"
  where
    getI k = m M.! k

getGates inps = map convert inps
  where
    convert g = createGate g 0

getByInputs gts inp = filter (\g -> S.member (x g) inp && S.member (y g) inp) gts

getOuts gts ins = foldr (\n s -> S.insert (z n) s) ins gts

onlyZs outs = S.size outs == length (filter (\x -> head x == 'z') $ S.toList outs)

sortGates gts ins sorted =
  let newGates = getByInputs gts ins
      newOuts = getOuts newGates ins
   in if onlyZs newOuts then sorted ++ newGates else sorted ++ newGates ++ sortGates gts newOuts sorted

initIns ins = foldr (\(x, _) s -> S.insert x s) S.empty ins

runGates :: [Gate] -> M.Map String Int -> M.Map String Int
runGates gs vals = foldl (\v g -> M.insert (z g) (getVal g v) v) vals gs

getZs out = filter (\(n, _) -> head n == 'z') out

convertToInt nums = foldl (\(s, p) x -> (s + x * 2 ^ p, p + 1)) (0, 0) betterNums
  where
    betterNums = map snd nums

data BF = BF {gts :: [Gate], vals :: M.Map String Int}

inVals g v = M.member (x g) v && M.member (y g) v

calcGate g bf = if inVals g (vals bf) then bf {gts = filter (/= g) (gts bf), vals = M.insert (z g) (getVal g (vals bf)) (vals bf)} else bf

bruteForce bf = if length (gts bf) > 0 then bruteForce (updateBf bf) else bf
  where
    updateBf bf = foldl (\b g -> calcGate g b) bf (gts bf)

main = do
  raw <- getArgs >>= readFile . head
  let lns = break null $ lines raw
  let ins = getInputs $ fst lns
  -- print ins
  let valMap = foldr (\(n, v) d -> M.insert n v d) M.empty ins
  let gs = getGates $ drop 1 (snd lns)
  -- print $ length gs
  -- let sgs = sortGates gs (initIns ins) []
  -- print $ length sgs
  -- let r = runGates sgs valMap
  let bf = bruteForce (BF {gts = gs, vals = valMap})
  let zs = getZs $ M.toList (vals bf)
  -- print zs
  -- print $ map snd zs
  print $ fst $ convertToInt zs
