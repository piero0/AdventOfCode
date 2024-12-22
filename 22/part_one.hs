import Data.Bits (xor)
import System.Environment (getArgs)

mix a b = (a `xor` b) `mod` 16777216

secret :: Int -> Int
secret x =
  let s1 = mix x (x * 64)
      s2 = mix s1 (floor (fromIntegral s1 / 32))
   in mix s2 (s2 * 2048)

multSecret t x
  | t == 0 = x
  | otherwise = multSecret (t - 1) (secret x)

main = do
  raw <- getArgs >>= readFile . head
  let nums = map (read :: String -> Int) $ lines raw
  print $ sum (map (multSecret 2000) nums)
