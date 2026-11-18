
<?php

header("Content-Type: application/json");


$conn = new mysqli(
    "localhost",
    "sato",
    "javier",
    "smart_plant"
);

if ($conn->connect_error) {

    http_response_code(500);

    echo json_encode([]);

    exit();
}

$conn->set_charset("utf8mb4");


$sql = "
    SELECT
        id,
        temperature,
        humidity,
        soil_moisture,
        light_status

    FROM sensor_data

    ORDER BY id DESC

    LIMIT 15
";

$result = $conn->query($sql);

if (!$result) {

    http_response_code(500);

    echo json_encode([]);

    $conn->close();

    exit();
}


$data = [];

while ($row = $result->fetch_assoc()) {

    $row["temperature"] = (float)$row["temperature"];

    $row["humidity"] = (float)$row["humidity"];

    $row["soil_moisture"] = (int)$row["soil_moisture"];

    $data[] = $row;
}


$data = array_reverse($data);


echo json_encode($data);


$result->free();

$conn->close();

?>
