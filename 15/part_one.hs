import Data.Map.Strict qualified as M
import Data.Set qualified as S

type Pair = (Int, Int)

data WareHouse = WH {robot :: Pair, walls :: S.Set Pair, boxes :: S.Set Pair} deriving (Show)

parseWarehouse :: [String] -> WareHouse -> WareHouse
parseWarehouse w wh = foldl parseRow wh $ zip [0 ..] w
  where
    parseRow wh (idx, row) = foldl (parseSymbol idx) wh $ zip [0 ..] row
    parseSymbol y wh (x, s)
      | s == '#' = wh {walls = S.insert (x, y) (walls wh)}
      | s == 'O' = wh {boxes = S.insert (x, y) (boxes wh)}
      | s == '@' = wh {robot = (x, y)}
      | otherwise = wh

moveBox s (x, y)
  | s == '^' = (x, y - 1)
  | s == '>' = (x + 1, y)
  | s == 'v' = (x, y + 1)
  | s == '<' = (x - 1, y)

isWall pos wh = S.member pos (walls wh)

isBox pos wh = S.member pos (boxes wh)

processBox dir orgpos newpos wh
  | isWall nextpos wh = wh
  | isBox nextpos wh = processBox dir orgpos nextpos wh
  | otherwise = swapBox
  where
    nextpos = moveBox dir newpos
    swapBox = wh {robot = orgpos, boxes = S.delete orgpos (S.insert nextpos (boxes wh))}

checkDest newpos pos dir wh
  | isWall newpos wh = wh
  | isBox newpos wh = processBox dir newpos newpos wh
  | otherwise = updatePos newpos
  where
    updatePos newpos = wh {robot = newpos}

makeAStep wh dir =
  let pos = robot wh
      newpos = moveBox dir pos
   in checkDest newpos pos dir wh

calcScore wh = sum $ map (\(x, y) -> x + 100 * y) $ S.toList (boxes wh)

main = do
  txt <- readFile "../data/2024/15/input"

  let lns = lines txt
  let warehouse = takeWhile (/= []) lns
  let moves = concat $ drop (length warehouse + 1) lns

  let wh = parseWarehouse warehouse (WH (0, 0) S.empty S.empty)
  let r = foldl makeAStep wh moves
  let score = calcScore r
  print score
