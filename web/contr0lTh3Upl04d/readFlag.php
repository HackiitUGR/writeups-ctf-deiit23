<?php
$filepath = "/flag.txt";
$file = fopen($filepath, "r");
if ($file) {
    echo fread($file, filesize($filepath));
    fclose($file);
}
?>