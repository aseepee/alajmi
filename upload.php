<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_FILES['fileToUpload'])) {
        $target_dir = "uploads/";
        $target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
        $uploadOk = 1;
        $imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

        // تحقق من نوع الملف
        if($imageFileType == "jpg" || $imageFileType == "png") {
            if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
                echo "تم رفع الملف بنجاح!";
            } else {
                echo "عذراً، حدث خطأ أثناء رفع الملف.";
            }
        } else {
            echo "الملف غير مسموح به.";
        }
    }
}
?>