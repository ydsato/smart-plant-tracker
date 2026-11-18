
<?php

header("Content-Type: application/json");

# connect to database
$conn = new mysqli(
    "localhost",
    "___",
    "____",
    "smart_plant"
);

if ($conn->connect_error) {

    http_response_code(500);

    echo json_encode([
        "status" => "error",
        "message" => "Database connection failed"
    ]);

    exit();
}

$conn->set_charset("utf8mb4");


$data = json_decode(
    file_get_contents("php://input"),
    true
);

if (
    !is_array($data) ||
    !isset(
        $data["temperature"],
        $data["humidity"],
        $data["soil_moisture"],
        $data["light_status"]
    )
) {

    http_response_code(400);

    echo json_encode([
        "status" => "error",
        "message" => "Invalid sensor data"
    ]);

    exit();
}


$temp = floatval($data["temperature"]);
$hum = floatval($data["humidity"]);
$soil = intval($data["soil_moisture"]);
$light = strval($data["light_status"]);

$stmt = $conn->prepare("
    INSERT INTO sensor_data
    (temperature, humidity, soil_moisture, light_status)
    VALUES (?, ?, ?, ?)
");

if (!$stmt) {

    http_response_code(500);

    echo json_encode([
        "status" => "error",
        "message" => "SQL preparation failed"
    ]);

    $conn->close();
    exit();
}

$stmt->bind_param(
    "ddis",
    $temp,
    $hum,
    $soil,
    $light
);

if ($stmt->execute()) {

    echo json_encode([
        "status" => "saved",
        "message" => "Sensor data successfully saved"
    ]);

} else {

    http_response_code(500);

    echo json_encode([
        "status" => "error",
        "message" => "Failed to save sensor data"
    ]);
}
$stmt->close();
$conn->close();

?>
