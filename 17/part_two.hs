import Data.Array (Array, array, (!))
import Data.Bits (xor)
import Data.Char (isDigit)
import Data.List (isSuffixOf)
import Debug.Trace (trace)

data VM = VM {ip :: Int, ar :: Int, br :: Int, cr :: Int, outp :: [Int], code :: [Int], inst :: Array Int (Int -> VM -> VM)}

instance Show VM where
  show (VM i a b c o _ _) = "ip " ++ show i ++ " a " ++ show a ++ " b " ++ show b ++ " c " ++ show c ++ " o " ++ show o

initVm ini inst vm =
  let ar = read (ini !! 0)
      br = read (ini !! 1)
      cr = read (ini !! 2)
      code = filter (>= 0) $ map (\x -> if isDigit x then read [x] :: Int else -1) $ last ini
   in VM {ip = 0, ar = ar, br = br, cr = cr, outp = [], code = code, inst = inst}

-- instructions helpers

cop x vm
  | x == 4 = ar vm
  | x == 5 = br vm
  | x == 6 = cr vm
  | otherwise = x

dv x vm =
  let af = fromIntegral $ ar vm
      opf = fromIntegral $ cop x vm
   in truncate $ af / (2 ** opf)

-- Program:
-- Register A: 33024962
-- 5,1,3,4,3,7,2,1,7
-- 2,4,1,3,7,5,1,5,0,3,4,2,5,5,3,0
--
-- 000
-- 011
-- B = A % 8 xor 3 xor 5 xor (A / 2 ^ (A % 8 * xor 3))
-- C = A / 2 ^ (A % 8 xor 3)
--
-- 2,4, B = A % 8
-- 1,3, B = B xor 3
-- 7,5, C = A / 2^B
-- 1,5, B = B xor 5
-- 4,2, B = B xor C
-- 5,5, out B % 8
-- 0,3, A = A / 8
-- 3,0, jnz 0

-- instructions
-- 0 x
adv x vm = trace ("adv " ++ show x ++ " " ++ show (ar vm)) (vm {ar = dv x vm})

-- 1 x
bxl x vm = trace ("bxl " ++ show x ++ " " ++ show (br vm)) (vm {br = br vm `xor` x})

-- 2 x
bst x vm = trace ("bst " ++ show x ++ " " ++ show (br vm)) (vm {br = cop x vm `mod` 8})

-- 3 x
jnz x vm = trace ("jnz " ++ show x ++ " " ++ show (ar vm)) (if ar vm == 0 then vm else vm {ip = x})

-- 4 x
bxc _ vm = trace ("bxc " ++ show (br vm) ++ " " ++ show (cr vm)) (vm {br = br vm `xor` cr vm})

-- 5 x
out x vm = trace ("out " ++ show x) (vm {outp = outp vm ++ [cop x vm `mod` 8]})

-- 6 x
bdv x vm = trace ("bdv " ++ show x ++ " " ++ show (br vm)) (vm {br = dv x vm})

-- 7 x
cdv x vm = trace ("cdv " ++ show x ++ " " ++ show (cr vm)) (vm {cr = dv x vm})

-- runtime :)

exec (ins, op) vm = (inst vm ! ins) op vm {ip = ip vm + 2}

runCmd [] vm = vm {ip = -1}
runCmd [a, b] vm = exec (a, b) vm

-- runVm insAr vm = trace ("cmd " ++ show nextCmd ++ " ip " ++ show (ip vm) ++ "\n" ++ show vm) (runCmd nextCmd vm insAr)
runVm vm = trace ("vm " ++ show vm) (runCmd nextCmd vm)
  where
    nextCmd = take 2 $ drop (ip vm) (code vm)

startVm vm = until stopCond runVm vm
  where
    stopCond v = ip v < 0

-- | | not (outp v `isSuffixOf` code v)
checkA vm a = trace ("check " ++ show a) (a, outp (startVm vm {ar = a}))

nextA vm a = filter (\(_, o) -> o `isSuffixOf` code vm) $ map (checkA vm) [a .. (a + 7)]

combNextA vm [] = []
combNextA vm (a : as) = nextA vm (8 * fst a) ++ combNextA vm as

findBackward vm a = until (hasSolution vm) (combNextA vm) a
  where
    hasSolution vm a = any id $ map (\(_, s) -> s == code vm) a

-- findBackward vm as = if outp vm == code vm then [a] else trace ("findBack " ++ show nextA) (map (findBackward vm . fst) nextA)

main = do
  -- txt <- readFile "../data/2024/17/test_input2"
  txt <- readFile "../data/2024/17/input"
  let ini = map (dropWhile (not . isDigit)) $ lines txt
  let insAr = array (0, 7) [(0, adv), (1, bxl), (2, bst), (3, jnz), (4, bxc), (5, out), (6, bdv), (7, cdv)]
  let vm = initVm ini insAr VM
  let a = 0
  -- let r = map (checkA vm) [a .. (a + 7)]
  -- let r = findBackward vm 0
  let r = findBackward vm [(0, [1])]
  print r
