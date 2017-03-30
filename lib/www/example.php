<?php

require_once 'jsonRPCClient.php';
$electrum_iop = new jsonRPCClient('http://localhost:7777');

echo '<b>Wallet balance</b><br />'."\n";
try {

    $balance = $electrum_iop->getbalance();
    echo 'confirmed: <i>'.$balance['confirmed'].'</i><br />'."\n";
    echo 'unconfirmed: <i>'.$balance['unconfirmed'].'</i><br />'."\n";

} catch (Exception $e) {
    echo nl2br($e->getMessage()).'<br />'."\n";
}

?>
