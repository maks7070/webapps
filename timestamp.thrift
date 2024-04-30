namespace py timestamp_service

struct Timestamp {
    1: required i64 unix_timestamp
}

service TimestampService {
    Timestamp getCurrentTimestamp(),
}