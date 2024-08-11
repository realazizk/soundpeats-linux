
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
    - read earbud setting: 00001002-0000-1000-8000-00805f9b34fb (anc , game mode)


- Services 

```
INFO:__main__:[Service] 0000a001-0000-1000-8000-00805f9b34fb (Handle: 19): Vendor specific
INFO:__main__:  [Characteristic] 00000008-0000-1000-8000-00805f9b34fb (Handle: 25): OBEX (read,notify), Value: bytearray(b'cd\x00')
INFO:__main__:    [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 27): Client Characteristic Configuration, Value: bytearray(b'\x00\x00')
INFO:__main__:  [Characteristic] 00000009-0000-1000-8000-00805f9b34fb (Handle: 34): Vendor specific (read,write-without-response), Value: bytearray(b'WQ00'), Max write w/o rsp size: 217
INFO:__main__:  [Characteristic] 00001001-0000-1000-8000-00805f9b34fb (Handle: 20): Browse Group Descriptor Service Class (write-without-response), Max write w/o rsp size: 217
INFO:__main__:  [Characteristic] 0000000b-0000-1000-8000-00805f9b34fb (Handle: 32): Vendor specific (read,write-without-response), Value: bytearray(b'\x00\x00\x00\x14\x00D\xfd2\x00\xf0\x00\xf2\xf9(\x00X\x022\x00<\x00@\x06\xa2\xfex\x00\xf0\nX\x02x\x00X\x1b\xf4\x01\x96\x004!\xa8\xfd,\x01\xb06X\x02d\x00h\x10j\xff,\x01'), Max write w/o rsp size: 217
INFO:__main__:  [Characteristic] 00000007-0000-1000-8000-00805f9b34fb (Handle: 28): ATT (read), Value: bytearray(b'SPTS04_20221202_V62')
INFO:__main__:  [Characteristic] 00001002-0000-1000-8000-00805f9b34fb (Handle: 22): Public Browse Root (read,notify), Error: Multiple Characteristics with this UUID, refer to your desired characteristic by the `handle` attribute instead.
INFO:__main__:    [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 24): Client Characteristic Configuration, Value: bytearray(b'\x00\x00')
INFO:__main__:  [Characteristic] 0000000d-0000-1000-8000-00805f9b34fb (Handle: 30): Vendor specific (read,write-without-response), Value: bytearray(b'\x01\x06\x02\x05\x03\x01\x04\x01\x05\x07\x06\x04\x07\x00\x08\x00\x00\x00\x00\x00'), Max write w/o rsp size: 217
INFO:__main__:[Service] 00001801-0000-1000-8000-00805f9b34fb (Handle: 4): Generic Attribute Profile
INFO:__main__:  [Characteristic] 00002a05-0000-1000-8000-00805f9b34fb (Handle: 5): Service Changed (indicate)
INFO:__main__:    [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 7): Client Characteristic Configuration, Value: bytearray(b'\x02\x00')
INFO:__main__:[Service] 00007033-0000-1000-8000-00805f9b34fb (Handle: 8): Vendor specific
INFO:__main__:  [Characteristic] 00002001-0000-1000-8000-00805f9b34fb (Handle: 14): Vendor specific (write-without-response), Max write w/o rsp size: 217
INFO:__main__:  [Characteristic] 00002002-0000-1000-8000-00805f9b34fb (Handle: 16): Vendor specific (notify)
INFO:__main__:    [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 18): Client Characteristic Configuration, Value: bytearray(b'\x00\x00')
INFO:__main__:  [Characteristic] 00001001-0000-1000-8000-00805f9b34fb (Handle: 9): Browse Group Descriptor Service Class (write-without-response), Max write w/o rsp size: 217
INFO:__main__:  [Characteristic] 00001002-0000-1000-8000-00805f9b34fb (Handle: 11): Public Browse Root (notify)
INFO:__main__:    [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 13): Client Characteristic Configuration, Value: bytearray(b'\x00\x00')
```

- Parse earbud setting

```java
public static Ccase getDataBean(int i, byte[] bArr) {
    switch (i) {
        case 4:
            Cconst cconst = f561catch;
            if (cconst == null) {
                f561catch = new Cconst(bArr);
            } else {
                cconst.setReceiveData(bArr);
            }
            return f561catch;
        case 5:
        case 10:
        case 11:
        case 14:
        case 15:
        case 19:
        case 20:
        case 21:
        case 25:
        case 26:
        case 27:
        default:
            return null;
        case 6:
            Cfinal cfinal = f571try;
            if (cfinal == null) {
                f571try = new Cfinal(bArr);
            } else {
                cfinal.setReceiveData(bArr);
            }
            return f571try;
        case 7:
            Ccatch ccatch = f568if;
            if (ccatch == null) {
                f568if = new Ccatch(0, bArr);
            } else {
                ccatch.setReceiveData(bArr);
            }
            return f568if;
        case 8:
            Cimport cimport = f569new;
            if (cimport == null) {
                f569new = new Cimport(bArr);
            } else {
                cimport.setReceiveData(bArr);
            }
            return f569new;
        case 9:
            Cgoto cgoto = f564else;
            if (cgoto == null) {
                f564else = new Cgoto(bArr);
            } else {
                cgoto.setReceiveData(bArr);
            }
            return f564else;
        case 12:
            Ccatch ccatch2 = f568if;
            if (ccatch2 == null) {
                f568if = new Ccatch(1, bArr);
            } else {
                ccatch2.m7467do(bArr);
            }
            return f568if;
        case 13:
            Cthrow cthrow = f559break;
            if (cthrow == null) {
                f559break = new Cthrow(bArr);
            } else {
                cthrow.setReceiveData(bArr);
            }
            return f559break;
        case 16:
            Csuper csuper = f560case;
            if (csuper == null) {
                f560case = new Csuper(bArr);
            } else {
                csuper.setReceiveData(bArr);
            }
            return f560case;
        case 17:
            Cnew cnew = f570this;
            if (cnew == null) {
                f570this = new Cnew(bArr);
            } else {
                cnew.setReceiveData(bArr);
            }
            return f570this;
        case 18:
            Cbreak cbreak = f567goto;
            if (cbreak == null) {
                f567goto = new Cbreak(bArr);
            } else {
                cbreak.setReceiveData(bArr);
            }
            return f567goto;
        case 22:
            Cif cif = f562class;
            if (cif == null) {
                f562class = new Cif(bArr);
            } else {
                cif.setReceiveData(bArr);
            }
            return f562class;
        case 23:
            Cdo cdo = f566for;
            if (cdo == null) {
                f566for = new Cdo(bArr);
            } else {
                cdo.setReceiveData(bArr);
            }
            return f566for;
        case 24:
            PairnameDataBean pairnameDataBean = f563const;
            if (pairnameDataBean == null) {
                f563const = new PairnameDataBean(bArr);
            } else {
                pairnameDataBean.setReceiveData(bArr);
            }
            return f563const;
        case 28:
            Cclass cclass = f565final;
            if (cclass == null) {
                f565final = new Cclass(bArr);
            } else {
                cclass.setReceiveData(bArr);
            }
            return f565final;
    }
}

public static ArrayList<Ccase> m7503do(byte[] bArr) {
    byte[] bArr2;
    ArrayList<Ccase> arrayList = new ArrayList<>();
    if (bArr != 0 && bArr.length >= 4) {
        int i = 2;
        if (bArr.length == bArr[1] + 2) {
            while (i < bArr.length) {
                int i2 = i + 1;
                int i3 = bArr[i];
                i += 2;
                int i4 = bArr[i2];
                if (i4 > 0) {
                    bArr2 = new byte[i4];
                    System.arraycopy(bArr, i, bArr2, 0, i4);
                    i += i4;
                } else {
                    bArr2 = null;
                }
                Ccase dataBean = Ccase.getDataBean(i3, bArr2);
                if (dataBean != null && !arrayList.contains(dataBean)) {
                    arrayList.add(dataBean);
                }
            }
        }
    }
    return arrayList;
}
```

- Device info
    - For the capsule3 pro GetDeviceInfoCapsule3Pro