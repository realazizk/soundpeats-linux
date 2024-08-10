
```java

    public void mo6724do(String str, UUID uuid, UUID uuid2, byte[] bArr, Cbreak cbreak) {
        Bundle bundle = new Bundle();
        bundle.putString("extra.mac", str);
        bundle.putSerializable("extra.service.uuid", uuid);
        bundle.putSerializable("extra.character.uuid", uuid2);
        bundle.putByteArray("extra.byte.value", bArr);
        m6999do(4, bundle, new Cconst(this, cbreak));
    }

    public class Ctry extends Ccase {
        public void mo7513do(Cfor cfor) {
            this.f656do = cfor;
            try {
                if (BluetoothManager.getConnectionState() == BluetoothProfile.STATE_CONNECTED) {
                    Intent intent = new Intent("DataRead");
                    intent.putExtra(DevFinal.STR.UUID, this.f630for);
                    context.sendBroadcast(intent);
                    //                   for           service        character                      
                    //  for
                    //  service   0000A001-0000-1000-8000-00805f9b34fb
                    //  character 00001002-0000-1000-8000-00805f9b34fb
                    this.f631if.mo6721do(this.f632new, Ccase.f629try, UUID.fromString(this.f630for), new Cfor(this));
                } else {
                    Cif.m7534if("BLE数据链路", "读取数据取消，未连接" + this.f632new + " 《《《《" + this.f630for);
                    m7543if();
                }
            } catch (Exception unused) {
                m7543if();
            }
        }
    }
    private static final String f507switch = "00001002-0000-1000-8000-00805f9b34fb";
    public void readEarbudSetting(String str) {
        readBleData(str, f507switch, new Cclass(this));
    }

```

- chars
    - get battery: 00000008-0000-1000-8000-00805f9b34fb
    - get version: 00000007-0000-1000-8000-00805f9b34fb
    - read eq: 0000000B-0000-1000-8000-00805f9b34fb
    - read button function: 0000000D-0000-1000-8000-00805f9b34fb
    - read earbud setting: 00001002-0000-1000-8000-00805f9b34fb


