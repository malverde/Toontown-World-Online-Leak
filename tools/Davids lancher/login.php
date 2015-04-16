<?php
if($_SERVER["HTTPS"] != "on")
{
    header("Location: https://" . $_SERVER["HTTP_HOST"] . $_SERVER["REQUEST_URI"]);
    exit();
}

$USERNAME = $_GET["n"];
$PASSWORD = $_GET["p"];

if(isset($_SERVER['HTTP_CF_CONNECTION_IP'])){
    $IP = $_SERVER['HTTP_CF_CONNECTING_IP'];
}
else{
    $IP = $_SERVER['REMOTE_ADDR'];
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
$DB_HOST = "localhost";
$DB_USER = "";
$DB_PASS = "";
$DB_DTBS = "";
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
$DB_CON = new mysqli($DB_HOST, $DB_USER, $DB_PASS, $DB_DTBS);
$LOGIN_ATT_SQL = mysqli_connect($DB_HOST, $DB_USER, $DB_PASS) or die("It failed.");
mysqli_select_db($LOGIN_ATT_SQL,$DB_DTBS);
if(mysqli_connect_errno()) {
    echo "Connection Failed: " . mysqli_connect_errno();
    exit();
}
$SALT = md5($PASSWORD);
$PASSWORD = hash('sha512', $PASSWORD.$SALT);
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
$TTW_DEVS_ONLY = 1;
sleep(1);
if($stmt = $DB_CON -> prepare("SELECT `ID`, `Username`, `Password`, `TOC`, `Verified`, `Group`, `Banned` FROM `users` WHERE (`Username`=? OR `EMail`=?) and `Password`=?")) {
    $stmt -> bind_param('sss', $USERNAME, $USERNAME, $PASSWORD);
    $stmt -> execute();
    $stmt -> bind_result($ID, $USERNAME, $PASSWORD, $TOC, $Verified, $Group, $Banned);
    $stmt -> fetch();
    if($ID >= 1){
        if($Banned == 1){
            mysqli_query($LOGIN_ATT_SQL,"INSERT INTO login_attempts (IP, Location, Username, Password, LoginCode) VALUES('$IP', 'TTW Launcher (Banned)', '$USERNAME', '$PASSWORD', 205)");
            mysqli_close($LOGIN_ATT_SQL);
            $stmt -> close();
            $DB_CON -> close();
            $loginArray = array('success' => false, 'reason' => 'This account is on hold. Please try again later.', 'errorCode' => 205);
            $loginJSON = json_encode($loginArray);
        }
        else if($Verified == 0){
            mysqli_query($LOGIN_ATT_SQL,"INSERT INTO login_attempts (IP, Location, Username, Password, LoginCode) VALUES('$IP', 'TTW Launcher (Unverified)', '$USERNAME', '$PASSWORD', 107)");
            mysqli_close($LOGIN_ATT_SQL);
            $stmt -> close();
            $DB_CON -> close();
            $loginArray = array('success' => false, 'reason' => 'This acccount isn\'t verified.', 'errorCode' => 107);
            $loginJSON = json_encode($loginArray);
        }
        else if($Group <= 100 and $TTW_DEVS_ONLY == 1){
            mysqli_query($LOGIN_ATT_SQL,"INSERT INTO login_attempts (IP, Location, Username, Password, LoginCode) VALUES('$IP', 'TTW Launcher (Invalid Group)', '$USERNAME', '$PASSWORD', 110)");
            mysqli_close($LOGIN_ATT_SQL);
            $stmt -> close();
            $DB_CON -> close();
            $loginArray = array('success' => false, 'reason' => 'Toontown world Online is currently not available for regular users. Please try again later.', 'errorCode' => 110);
            $loginJSON = json_encode($loginArray);
        }
        else{           
            mysqli_query($LOGIN_ATT_SQL,"INSERT INTO login_attempts (IP, Location, Username, Password, LoginCode) VALUES('$IP', 'TTW Launcher', '$USERNAME', '$PASSWORD', 1)");
            mysqli_query($LOGIN_ATT_SQL,"UPDATE `users` SET `LastLogin`=CURRENT_TIMESTAMP WHERE `Username`='$USERNAME'");
            mysqli_close($LOGIN_ATT_SQL);
            $stmt -> close();
            $DB_CON -> close();
            $TIME = time();
            $cookie = json_encode(array('userid' => $ID, 'timestamp' => $TIME, 'accesslevel' => $Group));
            $secret = '18d0d39be1b3fa05';
                $iv_size = mcrypt_get_iv_size(MCRYPT_RIJNDAEL_128, MCRYPT_MODE_CBC);
                $iv = mcrypt_create_iv($iv_size, MCRYPT_RAND);
                $cookie = $iv . mcrypt_encrypt(MCRYPT_RIJNDAEL_128, $secret, $cookie, MCRYPT_MODE_CBC, $iv);
            $cookie = base64_encode($cookie);
            $gameserver = "";
            $loginArray = array('success' => true, 'ttrgameserver' => $gameserver 'token' => $cookie);
            $loginJSON = json_encode($loginArray);
        }
    }
    else{
        mysqli_query($LOGIN_ATT_SQL,"INSERT INTO login_attempts (IP, Location, Username, Password, LoginCode) VALUES('$IP', 'TTW Launcher', '$USERNAME', '$PASSWORD', 105)");
        mysqli_close($LOGIN_ATT_SQL);
        $loginArray = array('success' => false, 'reason' => 'Invalid username and/or password. Please try again.', 'errorCode' => 105);
        $loginJSON = json_encode($loginArray);
    }
}
echo($loginJSON);

exit();
?>
