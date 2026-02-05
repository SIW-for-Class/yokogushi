CREATE TABLE IF NOT EXISTS tickets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  category TEXT NOT NULL,
  priority TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
);

-- 最低限の初期データ（あると動作確認が楽）
INSERT INTO tickets(title, body, category, priority, status)
VALUES
('VirtualBoxのGuest Additionsが入らない', 'ISOをマウントしてもunpackで失敗する。ログを確認したい。', 'linux', 'high', 'open'),
('SQLのLIKE検索が遅い', 'titleとbodyの検索で体感遅い。index貼るとどうなる？', 'db', 'normal', 'open');
