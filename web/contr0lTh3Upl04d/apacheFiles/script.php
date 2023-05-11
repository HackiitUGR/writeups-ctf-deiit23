<?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        // Check if the file was uploaded without errors
        if (isset($_FILES["file"]) && $_FILES["file"]["error"] == 0) {
            $allowed_extensions = array("jpg", "jpeg", "png", "gif");
            $file_name = $_FILES["file"]["name"];
            $extensions = explode(".", $file_name);
            if(count($extensions) == 1){
                echo "Sorry, there is an error, please check that the file has an extension.";
                echo "<br>";
                $file_extension = "";
            }
            else{
            	// Coge la primera extension (0 es el nombre del archivo)
            	$file_extension = strtolower($extensions[1]);            
            }
            
            // Check if the file is an image based on its extension
            if (in_array($file_extension, $allowed_extensions)) {
                // Upload file to the server
                $target_directory = "uploads/";
                $target_file = $target_directory . basename($_FILES["file"]["name"]);
                if (move_uploaded_file($_FILES["file"]["tmp_name"], $target_file)) {
                    echo "The file " . basename($_FILES["file"]["name"]) . " has been uploaded.";
                } else {
                    echo "Sorry, there was an error uploading your file.";
                }
            } else {
                echo "Sorry, only JPG, JPEG, PNG, and GIF files are allowed.";
                echo "<br>";
            }
        } else {
            echo "Sorry, there was an error uploading your file.";
            echo "<br>";
        }
    }
    ?>