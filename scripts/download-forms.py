#!/usr/bin/env python3
"""
Download IRS form PDFs into forms/<year>/

Usage: python3 scripts/download-forms.py [year]
Default year: 2025

Filters out:
  - Non-English language variants (Spanish, Russian, Korean, etc.)
  - IRS administrative/compliance forms (f12xxx-f15xxx series)
  - Year-stamped duplicates (e.g. f1099b--2025.pdf when f1099b.pdf exists)
"""

import os
import sys
import urllib.request
import urllib.error
import re

YEAR = sys.argv[1] if len(sys.argv) > 1 else "2025"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(SCRIPT_DIR, "..", "forms", YEAR)
BASE_URL = "https://www.irs.gov/pub/irs-pdf"

# Known non-English language suffixes appended to form names
LANG_SUFFIXES = {
    "sp", "ru", "ko", "zhs", "zht", "ar", "bn", "cs", "de", "fa", "fr",
    "gj", "gu", "ht", "it", "ja", "km", "kr", "pa", "pl", "pt", "so",
    "tl", "ur", "vn", "vie", "cn",
}

# Full list scraped from https://www.irs.gov/downloads/irs-pdf (all 63 pages)
ALL_FORMS = [
    "f1000.pdf","f1023ez.pdf","f1024.pdf","f1024a.pdf","f1028.pdf",
    "f10301.pdf","f1040.pdf","f1040c.pdf","f1040es.pdf","f1040esn.pdf",
    "f1040lep.pdf","f1040nr.pdf","f1040nra.pdf","f1040nrn.pdf","f1040nro.pdf",
    "f1040nrp.pdf","f1040nrs.pdf","f1040s.pdf","f1040s1.pdf","f1040s1a.pdf",
    "f1040s2.pdf","f1040s3.pdf","f1040s8.pdf","f1040sa.pdf","f1040sb.pdf",
    "f1040sc.pdf","f1040sd.pdf","f1040se.pdf","f1040sei.pdf","f1040sep.pdf",
    "f1040sf.pdf","f1040sh.pdf","f1040sj.pdf","f1040sr.pdf","f1040ss.pdf",
    "f1040sse.pdf","f1040v.pdf","f1040x.pdf",
    "f1041.pdf","f1041a.pdf","f1041es.pdf","f1041n.pdf","f1041qft.pdf",
    "f1041sd.pdf","f1041si.pdf","f1041sj.pdf","f1041sk1.pdf","f1041t.pdf",
    "f1041v.pdf",
    "f1042.pdf","f1042s.pdf","f1042sq.pdf","f1042t.pdf",
    "f1045.pdf",
    "f1065.pdf","f1065sb1.pdf","f1065sb2.pdf","f1065sc.pdf","f1065sd.pdf",
    "f1065sk1.pdf","f1065sk2.pdf","f1065sk3.pdf","f1065sm3.pdf","f1065x.pdf",
    "f1066.pdf","f1066sq.pdf",
    "f1094b.pdf","f1094c.pdf",
    "f1095a.pdf","f1095b.pdf","f1095c.pdf",
    "f1096.pdf",
    "f1097btc.pdf",
    "f1098.pdf","f1098c.pdf","f1098e.pdf","f1098f.pdf","f1098q.pdf","f1098t.pdf",
    "f1099a.pdf","f1099b--2025.pdf","f1099c.pdf","f1099cap.pdf",
    "f1099da.pdf","f1099da--2025.pdf","f1099div.pdf","f1099g.pdf","f1099h.pdf",
    "f1099int.pdf","f1099k.pdf","f1099ls.pdf","f1099ltc.pdf","f1099msc.pdf",
    "f1099nec.pdf","f1099oid.pdf","f1099ptr.pdf","f1099q.pdf","f1099qa.pdf",
    "f1099r.pdf","f1099s.pdf","f1099sa.pdf","f1099sb.pdf",
    "f1116.pdf","f1116sb.pdf","f1116sc.pdf","f1117.pdf","f1118.pdf",
    "f1118s1.pdf","f1118sj.pdf","f1118sk.pdf","f1118sl.pdf",
    "f1120.pdf","f1120c.pdf","f1120f.pdf","f1120h.pdf","f1120l.pdf",
    "f1120nd.pdf","f1120pc.pdf","f1120pol.pdf","f1120rei.pdf","f1120ric.pdf",
    "f1120s.pdf","f1120sb.pdf","f1120sd.pdf","f1120sf.pdf","f1120sg.pdf",
    "f1120sh.pdf","f1120sk2.pdf","f1120sk3.pdf","f1120sm3.pdf","f1120sn.pdf",
    "f1120so.pdf","f1120utp.pdf","f1120x.pdf",
    "f1122.pdf","f1125a.pdf","f1125e.pdf","f1127.pdf","f1128.pdf",
    "f1138.pdf","f1139.pdf",
    "f11c.pdf",
    "f172.pdf",
    "f2032.pdf","f2063.pdf","f2106.pdf","f2120.pdf","f2159.pdf",
    "f2210.pdf","f2210f.pdf","f2220.pdf","f2290.pdf","f2350.pdf",
    "f2438.pdf","f2439.pdf","f2441.pdf","f2553.pdf","f2555.pdf",
    "f2587.pdf","f2624.pdf","f2678.pdf","f2848.pdf",
    "f3115.pdf","f3468.pdf","f3491.pdf","f3520.pdf","f3520a.pdf",
    "f3800.pdf","f3800a.pdf","f3881.pdf","f3881a.pdf","f3903.pdf",
    "f3911.pdf","f3921.pdf","f3922.pdf","f3949a.pdf",
    "f4029.pdf","f4136.pdf","f4136sa.pdf","f4137.pdf","f4219.pdf",
    "f4255.pdf","f433a.pdf","f433aoi.pdf","f433b.pdf","f433boi.pdf",
    "f433d.pdf","f433f.pdf","f433h.pdf","f4361.pdf","f4421.pdf",
    "f4422.pdf","f4423.pdf","f4461.pdf","f4461a.pdf","f4461b.pdf","f4461c.pdf",
    "f4466.pdf","f4506.pdf","f4506a.pdf","f4506b.pdf","f4506c.pdf",
    "f4506f.pdf","f4506t.pdf","f4506tez.pdf","f4547.pdf","f4562.pdf",
    "f4563.pdf","f461.pdf","f4626.pdf","f4626sa.pdf","f4669.pdf","f4670.pdf",
    "f4684.pdf","f4720.pdf","f4768.pdf","f4797.pdf","f4808.pdf","f4810.pdf",
    "f4835.pdf","f4852.pdf","f4868.pdf","f4876a.pdf","f4952.pdf",
    "f4970.pdf","f4972.pdf","f4977.pdf",
    "f5074.pdf","f5129.pdf","f5213.pdf","f5227.pdf","f5300.pdf",
    "f5304sim.pdf","f5305.pdf","f5305a.pdf","f5305ase.pdf","f5305b.pdf",
    "f5305c.pdf","f5305e.pdf","f5305ea.pdf","f5305r.pdf","f5305ra.pdf",
    "f5305rb.pdf","f5305s.pdf","f5305sa.pdf","f5305sep.pdf","f5305sim.pdf",
    "f5306.pdf","f5306a.pdf","f5307.pdf","f5308.pdf","f5309.pdf","f5310.pdf",
    "f5310a.pdf","f5316.pdf","f5329.pdf","f5330.pdf","f5405.pdf","f5434.pdf",
    "f5434a.pdf","f5452.pdf","f5471.pdf","f5471se.pdf","f5471sg1.pdf",
    "f5471sh.pdf","f5471sh1.pdf","f5471si1.pdf","f5471sj.pdf","f5471sm.pdf",
    "f5471so.pdf","f5471sp.pdf","f5471sq.pdf","f5471sr.pdf",
    "f5472.pdf","f5495.pdf","f5498.pdf","f5498e.pdf","f5498qa.pdf","f5498sa.pdf",
    "f5500ez.pdf","f5558.pdf","f5578.pdf","f56.pdf","f5646.pdf","f5695.pdf",
    "f56f.pdf","f5713.pdf","f5713sa.pdf","f5713sb.pdf","f5713sc.pdf",
    "f5735.pdf","f5754.pdf","f5768.pdf","f5884.pdf","f5884a.pdf",
    "f5884c.pdf","f5884d.pdf",
    "f6069.pdf","f6088.pdf","f6112.pdf","f6118.pdf","f6197.pdf","f6198.pdf",
    "f6251.pdf","f6252.pdf","f637.pdf","f6478.pdf","f6497.pdf","f6524.pdf",
    "f656.pdf","f656b.pdf","f656l.pdf","f656ppv.pdf","f6627.pdf",
    "f6729c.pdf","f6729d.pdf","f673.pdf","f6744.pdf","f6765.pdf","f6781.pdf",
    "f7004.pdf","f7036.pdf",
    "f706.pdf","f706a.pdf","f706ce.pdf","f706gsd.pdf","f706gsd1.pdf",
    "f706gst.pdf","f706na.pdf","f706qdt.pdf","f706sa.pdf","f706sb.pdf",
    "f706sc.pdf","f706sd.pdf","f706se.pdf","f706sf.pdf","f706sg.pdf",
    "f706sh.pdf","f706si.pdf","f706sj.pdf","f706sk.pdf","f706sl.pdf",
    "f706sm.pdf","f706so.pdf","f706sq.pdf","f706sr.pdf","f706sr1.pdf",
    "f706st.pdf","f706su.pdf","f706sw.pdf",
    "f708.pdf","f709.pdf","f709na.pdf","f712.pdf",
    "f720.pdf","f7200.pdf","f720cs.pdf","f720to.pdf","f720x.pdf",
    "f7203.pdf","f7204.pdf","f7205.pdf","f7206.pdf","f7207.pdf","f7208.pdf",
    "f7210.pdf","f7211.pdf","f7213.pdf","f7217.pdf","f7218.pdf","f7220.pdf",
    "f730.pdf",
    "f8023.pdf","f8027.pdf","f8027t.pdf","f8038.pdf","f8038b.pdf",
    "f8038cp.pdf","f8038cpa.pdf","f8038g.pdf","f8038gc.pdf","f8038r.pdf",
    "f8038t.pdf","f8038tc.pdf","f8050.pdf","f8082.pdf","f8233.pdf",
    "f8274.pdf","f8275.pdf","f8275r.pdf","f8281.pdf","f8282.pdf",
    "f8283.pdf","f8283v.pdf","f8288.pdf","f8288a.pdf","f8288b.pdf","f8288c.pdf",
    "f8300.pdf","f8302.pdf","f8308.pdf","f8316.pdf","f8328.pdf","f8329.pdf",
    "f8330.pdf","f8332.pdf","f8379.pdf","f8396.pdf","f8404.pdf","f843.pdf",
    "f8453.pdf","f8498.pdf","f8508.pdf","f8508i.pdf","f851.pdf",
    "f8546.pdf","f8554.pdf","f8554ep.pdf","f8582.pdf","f8582cr.pdf",
    "f8586.pdf","f8594.pdf","f8596.pdf","f8596a.pdf","f8606.pdf",
    "f8609.pdf","f8609a.pdf","f8610.pdf","f8610sa.pdf","f8611.pdf",
    "f8612.pdf","f8613.pdf","f8615.pdf","f8621.pdf","f8621a.pdf",
    "f8653.pdf","f8654.pdf","f8655.pdf","f8689.pdf","f8691.pdf","f8697.pdf",
    "f8703.pdf","f8716.pdf","f8717.pdf","f8717a.pdf","f8718.pdf","f8725.pdf",
    "f872b.pdf","f8752.pdf","f8796a.pdf","f8801.pdf","f8802.pdf","f8804.pdf",
    "f8804c.pdf","f8804sa.pdf","f8804w.pdf","f8805.pdf","f8806.pdf",
    "f8809.pdf","f8809ex.pdf","f8809i.pdf","f8810.pdf","f8811.pdf",
    "f8813.pdf","f8814.pdf","f8815.pdf","f8818.pdf","f8819.pdf","f8820.pdf",
    "f8821.pdf","f8821a.pdf","f8822.pdf","f8822b.pdf","f8823.pdf","f8824.pdf",
    "f8825.pdf","f8825sa.pdf","f8826.pdf","f8827.pdf","f8828.pdf","f8829.pdf",
    "f8830.pdf","f8831.pdf","f8832.pdf","f8833.pdf","f8834.pdf","f8835.pdf",
    "f8838.pdf","f8838p.pdf","f8839.pdf","f8840.pdf","f8842.pdf","f8843.pdf",
    "f8844.pdf","f8846.pdf","f8848.pdf","f8849.pdf","f8849s1.pdf","f8849s2.pdf",
    "f8849s3.pdf","f8849s5.pdf","f8849s6.pdf","f8849s8.pdf","f8851.pdf",
    "f8853.pdf","f8854.pdf","f8855.pdf","f8857.pdf","f8858.pdf","f8858sm.pdf",
    "f8859.pdf","f8862.pdf","f8863.pdf","f8864.pdf","f8865.pdf","f8865sg.pdf",
    "f8865sh.pdf","f8865sk1.pdf","f8865sk2.pdf","f8865sk3.pdf","f8865so.pdf",
    "f8866.pdf","f8867.pdf","f8868.pdf","f8869.pdf","f8870.pdf","f8872.pdf",
    "f8873.pdf","f8874.pdf","f8874a.pdf","f8874b.pdf","f8875.pdf","f8876.pdf",
    "f8878.pdf","f8878a.pdf","f8879.pdf","f8879c.pdf","f8879eg.pdf",
    "f8879f.pdf","f8879s.pdf","f8879ta.pdf","f8879te.pdf","f8879wh.pdf",
    "f8880.pdf","f8881.pdf","f8882.pdf","f8883.pdf","f8885.pdf","f8886.pdf",
    "f8886t.pdf","f8888.pdf","f8889.pdf","f8892.pdf","f8896.pdf","f8898.pdf",
    "f8899.pdf","f8900.pdf","f8902.pdf","f8903.pdf","f8904.pdf","f8905.pdf",
    "f8906.pdf","f8908.pdf","f8911.pdf","f8911sa.pdf","f8912.pdf",
    "f8915b.pdf","f8915d.pdf","f8915f.pdf","f8916.pdf","f8916a.pdf",
    "f8917.pdf","f8918.pdf","f8919.pdf","f8922.pdf","f8924.pdf","f8925.pdf",
    "f8927.pdf","f8928.pdf","f8932.pdf","f8933.pdf","f8933sa.pdf","f8933sb.pdf",
    "f8933sc.pdf","f8933sd.pdf","f8933se.pdf","f8933sf.pdf","f8936.pdf",
    "f8936sa.pdf","f8937.pdf","f8938.pdf","f8940.pdf","f8941.pdf","f8944.pdf",
    "f8945.pdf","f8946.pdf","f8947.pdf","f8948.pdf","f8949.pdf","f8950.pdf",
    "f8951.pdf","f8952.pdf","f8955ssa.pdf","f8957.pdf","f8958.pdf",
    "f8959.pdf","f8960.pdf","f8962.pdf","f8963.pdf","f8966.pdf","f8966c.pdf",
    "f8971.pdf","f8971sa.pdf","f8973.pdf","f8974.pdf","f8975.pdf","f8975sa.pdf",
    "f8978.pdf","f8978sa.pdf","f8979.pdf","f8980.pdf","f8981.pdf","f8982.pdf",
    "f8983.pdf","f8984.pdf","f8985.pdf","f8985v.pdf","f8986.pdf","f8988.pdf",
    "f8989.pdf","f8990.pdf","f8991.pdf","f8992.pdf","f8992sa.pdf","f8992sb.pdf",
    "f8993.pdf","f8994.pdf","f8995.pdf","f8995a.pdf","f8995aa.pdf",
    "f8995ab.pdf","f8995ac.pdf","f8995ad.pdf","f8996.pdf","f8997.pdf",
    "f9000.pdf",
    "f907.pdf","f911.pdf","f921.pdf","f9210.pdf","f9212.pdf","f9214.pdf",
    "f921a.pdf","f921i.pdf","f921m.pdf","f921p.pdf","f9249.pdf","f9250.pdf",
    "f926.pdf","f928.pdf","f9325.pdf","f9368.pdf",
    "f940.pdf","f940b.pdf","f940sa.pdf","f940sr.pdf",
    "f941.pdf","f941sb.pdf","f941sd.pdf","f941sr.pdf","f941x.pdf",
    "f943.pdf","f943a.pdf","f943sr.pdf","f943x.pdf",
    "f944.pdf","f944x.pdf",
    "f945.pdf","f945a.pdf","f945x.pdf",
    "f9423.pdf","f9465.pdf","f952.pdf","f9549.pdf",
    "f965a.pdf","f965b.pdf","f965c.pdf","f965d.pdf","f965e.pdf",
    "f965sd.pdf","f965sf.pdf","f965sh.pdf",
    "f966.pdf","f9661.pdf","f970.pdf","f972.pdf","f973.pdf","f976.pdf",
    "f9779.pdf","f9783.pdf","f982.pdf",
    "f990.pdf","f990bl.pdf","f990ez.pdf","f990ezb.pdf","f990pf.pdf",
    "f990sa.pdf","f990sc.pdf","f990sd.pdf","f990se.pdf","f990sf.pdf",
    "f990sg.pdf","f990sh.pdf","f990si.pdf","f990sj.pdf","f990sk.pdf",
    "f990sl.pdf","f990sm.pdf","f990sn.pdf","f990so.pdf","f990sr.pdf",
    "f990t.pdf","f990tsa.pdf",
    # W-forms
    "fw2.pdf","fw2as.pdf","fw2c.pdf","fw2g.pdf","fw2vi.pdf",
    "fw3.pdf","fw3c.pdf","fw3ss.pdf",
    "fw4.pdf","fw4p.pdf","fw4r.pdf","fw4s.pdf","fw4v.pdf",
    "fw7.pdf","fw7a.pdf","fw8ben.pdf","fw8bene.pdf","fw8eci.pdf",
    "fw8exp.pdf","fw8imy.pdf","fw9.pdf",
]

def is_lang_variant(fname):
    """Return True if filename appears to be a non-English language variant."""
    base = fname.replace(".pdf", "")
    for suffix in LANG_SUFFIXES:
        if base.endswith(suffix):
            # Make sure the root form exists (e.g. f1040sp -> f1040)
            root = base[: -len(suffix)]
            if root + ".pdf" in ALL_FORMS_SET or root:
                return True
    return False

ALL_FORMS_SET = set(ALL_FORMS)

def should_skip(fname):
    """Return True if this form should be skipped."""
    base = fname.replace(".pdf", "")
    # Skip clear language variants
    for suffix in sorted(LANG_SUFFIXES, key=len, reverse=True):
        if base.endswith(suffix) and len(base) > len(suffix) + 2:
            return True
    return False

def download(url, dest_path):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(dest_path, "wb") as f:
            f.write(data)
        return len(data)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise

def human_size(n):
    if n < 1024:
        return f"{n}B"
    if n < 1024 * 1024:
        return f"{n // 1024}KB"
    return f"{n / (1024*1024):.1f}MB"

def main():
    os.makedirs(DEST, exist_ok=True)

    to_download = [f for f in ALL_FORMS if not should_skip(f)]
    print(f"Downloading {len(to_download)} IRS forms for tax year {YEAR} into {DEST}/")
    print()

    passed = 0
    failed = 0
    skipped = 0

    for fname in to_download:
        dest_path = os.path.join(DEST, fname)
        url = f"{BASE_URL}/{fname}"

        if os.path.exists(dest_path):
            print(f"  {fname:<50} skipped (exists)")
            skipped += 1
            continue

        size = download(url, dest_path)
        if size is not None:
            print(f"  {fname:<50} OK ({human_size(size)})")
            passed += 1
        else:
            print(f"  {fname:<50} 404")
            failed += 1

    print()
    print(f"Done: {passed} downloaded, {skipped} already present, {failed} not found.")

if __name__ == "__main__":
    main()
