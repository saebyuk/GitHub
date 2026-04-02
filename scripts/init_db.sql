CREATE TABLE IF NOT EXISTS pki_operation_history (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  event_time DATETIME NOT NULL,
  system_name VARCHAR(64) NOT NULL,
  module_name VARCHAR(64) NOT NULL,
  severity VARCHAR(16) NOT NULL,
  error_code VARCHAR(32) NOT NULL,
  message TEXT NOT NULL,
  operator_id VARCHAR(32) NOT NULL,
  host_name VARCHAR(64) NOT NULL,
  action_result VARCHAR(16) NOT NULL
);

CREATE TABLE IF NOT EXISTS qa_query_history (
  query_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id VARCHAR(32) NOT NULL,
  question TEXT NOT NULL,
  answer_summary TEXT NOT NULL,
  mode ENUM('rag', 'llm_only', 'db_nl') NOT NULL,
  latency_ms INT NOT NULL,
  tokens_in INT NOT NULL DEFAULT 0,
  tokens_out INT NOT NULL DEFAULT 0,
  device_type VARCHAR(32) NOT NULL DEFAULT 'unknown',
  npu_enabled BOOLEAN NOT NULL DEFAULT FALSE,
  created_at DATETIME NOT NULL
);
