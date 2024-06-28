<?php
    $encryptedCookie = 'session cookie';

    $appKey = 'dQ5xJ4ZRFWONV2cxU1PWa5gaLSs57Bq7GULxannqCyo=';

    $cipher = 'AES-256-CBC';
    
    $ivSize = openssl_cipher_iv_length($cipher);
    $iv = substr(base64_decode($encryptedCookie), 0, $ivSize);
    
    $payload = substr(base64_decode($encryptedCookie), $ivSize);
    $decryptedPayload = openssl_decrypt($payload, $cipher, $appKey, OPENSSL_RAW_DATA, $iv);
    
    if ($decryptedPayload !== false) {
	    $sessionData = unserialize($decryptedPayload);
	    var_dump($sessionData);
    } 
?>

