<?php

function saludar($nombre) {
    if ($nombre == "Angel") {
        echo "Hola, " . $nombre;
    } else {
        echo 'Hola, visitante';
    }

    return true;
}

$contador = 3;
while ($contador > 0) {
    $contador = $contador - 1;
}

?>