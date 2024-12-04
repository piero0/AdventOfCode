import Data.Char (isDigit)
import Text.ParserCombinators.ReadP

getMul :: ReadP (Int, Int)
getMul = do
  string "mul("
  d1 <- fmap read $ many1 $ satisfy isDigit
  string ","
  d2 <- fmap read $ many1 $ satisfy isDigit
  string ")"
  return (d1, d2)

parsePart1 :: String -> [(Int, Int)] -> [(Int, Int)]
parsePart1 [] nums = nums
parsePart1 content nums =
  case readP_to_S getMul content of
    [] -> parsePart1 (tail content) nums
    [(x, rest)] -> parsePart1 rest [x] ++ nums
    _ -> error "Oww"

main = do
  content <- readFile "../data/2024/3/input"
  -- print content
  let resp = parsePart1 content []
  let total = sum $ map (uncurry (*)) resp
  print total
