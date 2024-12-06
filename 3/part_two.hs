import Data.Char (isDigit)
import Text.ParserCombinators.ReadP

data Mul = Mul {x :: Int, tot :: Int, on :: Bool} deriving (Show)

getMul :: ReadP Mul
getMul = do
  string "mul("
  d1 <- fmap read $ many1 $ satisfy isDigit
  string ","
  d2 <- fmap read $ many1 $ satisfy isDigit
  string ")"
  return (Mul (d1 * d2) 0 False)

getDo = do
  string "do()"
  return (Mul 0 0 True)

getDont = do
  string "don't()"
  return (Mul 0 0 False)

sumMul nv tt
  | x nv == 0 = Mul 0 (tot tt) (on nv)
  | otherwise = Mul 0 (if on tt then x nv + tot tt else tot tt) (on tt)

parsePart2 [] total = total
parsePart2 content total =
  case readP_to_S (getMul <++ getDont <++ getDo) content of
    [] -> parsePart2 (tail content) total
    [(cur, rest)] -> parsePart2 rest $ sumMul cur total
    _ -> error "Oww"

main = do
  content <- readFile "../data/2024/3/input"
  let resp = parsePart2 content (Mul 0 0 True)
  print (tot resp)
