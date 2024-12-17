import Data.Array (array, (!))
import Data.Bits (xor)
import Data.Char (isDigit)

data VM = VM {ip :: Int, ar :: Int, br :: Int, cr :: Int, outp :: [Int], code :: [Int]} deriving (Show)

initVm ini vm =
  let ar = read (ini !! 0)
      br = read (ini !! 1)
      cr = read (ini !! 2)
      code = filter (>= 0) $ map (\x -> if isDigit x then read [x] :: Int else -1) $ last ini
   in VM {ip = 0, ar = ar, br = br, cr = cr, outp = [], code = code}

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

-- instructions

adv x vm = vm {ar = dv x vm}

bxl x vm = vm {br = br vm `xor` x}

bst x vm = vm {br = cop x vm `mod` 8}

jnz x vm = if ar vm == 0 then vm {ip = x} else vm

bxc _ vm = vm {br = br vm `xor` cr vm}

out x vm = vm {outp = outp vm ++ [cop x vm `mod` 8]}

bdv x vm = vm {br = dv x vm}

cdv x vm = vm {cr = dv x vm}

-- runtime :)

exec (ins, op) vm insAr = (insAr ! ins) op vm

runVm vm = vm

main = do
  txt <- readFile "../data/2024/17/test_input"
  let ini = map (dropWhile (not . isDigit)) $ lines txt
  let vm = initVm ini VM
  let insAr = array (0, 7) [(0, adv), (1, bxl), (2, bst), (3, jnz), (4, bxc), (5, out), (6, bdv), (7, cdv)]
  let r = outp $ until (\vm -> ip vm == 0) runVm vm
  print r
