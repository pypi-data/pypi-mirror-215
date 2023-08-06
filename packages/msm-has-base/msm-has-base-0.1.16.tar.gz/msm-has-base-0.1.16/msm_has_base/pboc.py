import random

from typing import Dict
from datetime import datetime
from loguru import logger

from .bc_info import BCInfo
from . import tlv


class PBOC(object):
    def __init__(self, runner):
        super(PBOC, self).__init__()
        self.exec = runner

    def run(self, cmd: str) -> Dict:
        logger.debug("cmd: {}", cmd)
        resp = self.exec(cmd)
        result = tlv.decode(bytes.fromhex(resp), flatten=True)
        logger.debug("result: {}", result)
        return result

    def select(self, name: str, next=False) -> Dict:
        cmd = (
            "00a404"
            + ("02" if next else "00")
            + "{:02x}".format(len(name) // 2)
            + name
            + "ff"
        )
        return self.run(cmd)

    def read_record(self, sfi: int, idx: int) -> Dict:
        ctl = "{:02x}".format(sfi << 3 ^ 4)
        cmd = "00b2" + "{:02x}".format(idx) + ctl
        return self.run(cmd)

    def get_aids(self, sfi: int) -> list:
        aids = []
        for i in range(1, 16):
            try:
                result = self.read_record(sfi, i)
                aid = result["4F"].hex()
                if aid not in aids:
                    aids.append(aid)
            except:
                break

        logger.debug("aids: {}", aids)
        return aids

    def gpo(self, pdol: bytes, money: int) -> Dict:
        # PDOL
        # 工行 9f7a 01 9f02 06 5f2a 02
        # 农行         9f02 06 5f2a 02 df69 01
        # 建行 9f7a 01 9f02 06 5f2a 02
        # 中行 9f7a 01 9f02 06 5f2a 02 df69 01
        # 交通 9f7a 01 9f02 06 5f2a 02 df69 01
        # 广发 9f7a 01 9f02 06 5f2a 02 df69 01
        # 中原 9f7a 01 9f02 06 5f2a 02
        # 华夏 9f7a 01 9f02 06 5f2a 02 df69 01
        # 平安 9f7a 01 9f02 06 5f2a 02
        logger.debug("pdol: {}", pdol)
        gpo_cmd = ""
        if b"\x9F\x7A" in pdol:
            gpo_cmd += "ff"
        if b"\x9F\x02" in pdol:
            gpo_cmd += "{:012x}".format(money)
        if b"\x5F\x2A" in pdol:
            gpo_cmd += "0156"
        if b"\xDF\x69" in pdol:
            gpo_cmd += "00"

        gpo_len = len(gpo_cmd) // 2

        cmd = (
            "80a80000"
            + "{:02x}".format(gpo_len + 2)
            + "83"
            + "{:02x}".format(gpo_len)
            + gpo_cmd
            + "ff"
        )
        return self.run(cmd)

    def read_records(self, afl: bytes) -> Dict:
        result = {}
        i = 0
        while i < len(afl):
            part = afl[i : i + 4]

            sfi = part[0] >> 3
            j = part[1]
            e = part[2]
            while j <= e:
                resp = self.read_record(sfi, j)
                result.update(resp)
                j += 1

            i += 4

        return result

    def get_data(self, tag: str) -> Dict:
        return self.run("80ca" + tag)

    def ac(self, cdol1: bytes, amount: int, trade: str, merchant: str = "") -> Dict:
        cmd: bytes = b""

        d_9f02 = None
        if b"\x9f\x02" in cdol1:
            d_9f02 = amount.to_bytes(6, "big")
            cmd += d_9f02

        if b"\x9f\x03" in cdol1:
            cmd += (0).to_bytes(6, "big")

        if b"\x9f\x1a" in cdol1:
            cmd += b"\x01\x56"

        d_95 = None
        if b"\x95" in cdol1:
            d_95 = b"\x00\x00\x80\x00\x00"
            cmd += d_95

        if b"\x5f\x2a" in cdol1:
            cmd += b"\x01\x56"

        d_9a = None
        if b"\x9a" in cdol1:
            d_9a = bytes.fromhex(datetime.now().strftime("%y%m%d"))
            cmd += d_9a

        d_9c = None
        if b"\x9c" in cdol1:
            d_9c = bytes.fromhex(trade)
            cmd += d_9c

        d_9f37 = None
        if b"\x9f\x37" in cdol1:
            d_9f37 = random.randint(1000000000, 2000000000).to_bytes(4, "big")
            cmd += d_9f37

        if b"\x9f\x21" in cdol1:
            cmd += bytes.fromhex(datetime.now().strftime("%H%M%S"))

        if b"\x9f\x4e" in cdol1:
            if merchant is None:
                cmd += (0).to_bytes(14, "big")
            else:
                cmd += bytes.fromhex(merchant)

        cmd += (0).to_bytes(52 - len(cmd), "big")
        cmd = b"\x80\xae\x80\x00\x34" + cmd + b"\xff"
        result = self.run(cmd.hex())

        if "80" in result:
            result.update({"9F27": result["80"][:1], "9F26": result["80"][3:11]})
            if len(result["80"]) > 11:
                result.update({"9F10": result["80"][11:]})

        result.update(
            {
                "9F37": d_9f37,
                "95": d_95,
                "9A": d_9a,
                "9C": d_9c,
                "9F02": d_9f02,
                "5F2A": b"\x01\x56",
                "9F1A": b"\x01\x56",
                "9F03": (0).to_bytes(6, "big"),
                "9F33": b"\x00\x40\x00",
            }
        )
        logger.debug("ac result: {}", result)
        return result

    def read_info(self, amount: int, trade: str, merchant: str = "") -> BCInfo:
        records = {}

        r = self.select("315041592e5359532e4444463031")
        logger.debug(r)

        sfi = r["88"][0]
        aids = self.get_aids(sfi)

        for i in range(len(aids)):
            r = self.select(aids[i], i > 0)

            pdol = r["9F38"]
            r = self.gpo(pdol, amount)

            aip = r["80"][:2]
            afls = r["80"][2:]
            records = self.read_records(afls)

            records["82"] = aip

        d_9f13 = self.get_data("9F13")
        records.update(d_9f13)

        d_9f36 = self.get_data("9F36")
        records.update(d_9f36)

        cdol1 = records["8C"]
        r = self.ac(cdol1, amount, trade, merchant)
        records.update(r)

        logger.debug("records: {}", records)

        d_55_list = (
            b"\x9f\x26",
            b"\x08",
            records["9F26"],
            b"\x9f\x27",
            b"\x01",
            records["9F27"],
            b"\x9f\x10",
            (len(records["9F10"])).to_bytes(1, "big"),
            records["9F10"],
            b"\x9f\x37",
            b"\x04",
            records["9F37"],
            b"\x9f\x36",
            b"\x02",
            records["9F36"],
            b"\x95",
            b"\x05",
            records["95"],
            b"\x9a",
            b"\x03",
            records["9A"],
            b"\x9c",
            b"\x01",
            records["9C"],
            b"\x9f\x02",
            b"\x06",
            records["9F02"],
            b"\x5f\x2a",
            b"\x02",
            records["5F2A"],
            b"\x82",
            b"\x02",
            records["82"],
            b"\x9f\x1a",
            b"\x02",
            records["9F1A"],
            b"\x9f\x03",
            b"\x06",
            records["9F03"],
            b"\x9f\x33",
            b"\x03",
            records["9F33"],
        )

        result: BCInfo = BCInfo()
        result.ic55 = b"".join(d_55_list).hex()
        result.track2 = records["57"].hex()
        result.pan = records["5A"].hex()
        result.pan_sn = records["5F34"].hex()
        logger.debug("result: {}", result)
        return result
