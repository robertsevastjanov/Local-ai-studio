<?php

header('Content-Type: application/json; charset=utf-8');

try {$dbPath = __DIR__ . '/../history.db';

    if (!file_exists($dbPath)) {
        throw new RuntimeException('Database not found');
    }

    $pdo = new PDO('sqlite:' . $dbPath);

    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $statement = $pdo->query("
        SELECT
            COUNT(*) AS total_generations,
            COUNT(DISTINCT seed) AS unique_seeds,
            COUNT(
                CASE
                    WHEN DATE(created_at) = DATE('now')
                    THEN 1
                END
            ) AS generations_today
        FROM generations
    ");

    $stats = $statement->fetch(PDO::FETCH_ASSOC);

    $stats = array_map('intval', $stats);

    echo json_encode([
        'status' => 'ok',
        'stats' => $stats
    ]);

} catch (PDOException | RuntimeException $error) {

    http_response_code(500);

    echo json_encode([
        'status' => 'error',
        'message' => 'Statistics unavailable'
    ]);
}