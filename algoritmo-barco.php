<?php

function clasificar($numero) {
    if ($numero % 2 === 0) {
        return "par";
    }
    return "impar";
}

$suma = 0;
$producto = 1;

for ($i = 1; $i <= 5; $i++) {
    $suma += $i;
    $producto *= $i;
}

$resto = 10;
while ($resto > 0) {
    $resto -= 3;
}

$contador = 5;
$contador--;

echo "Suma: " . $suma;
echo "Producto: " . $producto;
echo clasificar($suma);

?>
