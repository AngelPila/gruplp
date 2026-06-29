<?php

$base = 10;
$altura = 5;

function area($b, $h) {
    $resultado = $b * $h;
    return $resultado;
}

function perimetro($b, $h) {
    $suma = $b + $h;
    return $suma * 2;
}

$areaTotal = area($base, $altura);
$perimetroTotal = perimetro($base, $altura);

echo $areaTotal;
echo $perimetroTotal;

?>
