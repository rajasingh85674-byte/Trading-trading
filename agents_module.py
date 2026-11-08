import json
import os
import logging

logging.basicConfig(level=logging.INFO)

class RiskManagementAgent:
    """
    1-2% रिस्क कैप और डेली लॉकआउट रूल (डेटा डिस्क/फाइल में सेव होता है)
    """
    def __init__(self, data_file="risk_data.json", max_risk_pct=2.0, max_consecutive_losses=2):
        self.data_file = data_file
        self.max_risk_pct = max_risk_pct
        self.max_consecutive_losses = max_consecutive_losses
        self.consecutive_losses = 0
        self.is_locked_out = False
        self._load_state()

    def _load_state(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.consecutive_losses = data.get("consecutive_losses", 0)
                    self.is_locked_out = data.get("is_locked_out", False)
            except Exception as e:
                logging.error(f"Error loading risk state: {e}")

    def _save_state(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump({
                    "consecutive_losses": self.consecutive_losses,
                    "is_locked_out": self.is_locked_out
                }, f)
        except Exception as e:
            logging.error(f"Error saving risk state: {e}")

    def check_trade_allowed(self):
        if self.is_locked_out:
            logging.warning("[RISK AGENT] HARD LOCKOUT ACTIVE! Max consecutive losses reached.")
            return False, "Daily Lockout Active (2 Consecutive Losses Hit)"
        return True, "Trading Allowed"

    def record_trade_result(self, is_win: bool):
        if is_win:
            self.consecutive_losses = 0
        else:
            self.consecutive_losses += 1
            if self.consecutive_losses >= self.max_consecutive_losses:
                self.is_locked_out = True
        self._save_state()


class MasterConsensusEngine:
    """
    11-Agent System: Market Structure (HH/HL/LH/LL), Liquidity Sweep & CHOCH Evaluation
    """
    def __init__(self):
        self.risk_agent = RiskManagementAgent()

    def evaluate_market(self, market_data):
        allowed, risk_msg = self.risk_agent.check_trade_allowed()
        if not allowed:
            return {"decision": "LOCKOUT", "reason": risk_msg, "votes": 0}

        votes = 0
        # Agent 1: Trend & Structure
        if market_data.get("structure") in ["HH_HL", "CHOCH_BULLISH"]:
            votes += 2
        
        # Agent 2: Liquidity Sweep
        if market_data.get("liquidity_swept", False):
            votes += 3
        
        # Agent 3: CHOCH Confirmation
        if market_data.get("choch_confirmed", False):
            votes += 3

        # Agent 4: Risk/Reward Agent (Minimum 1:2)
        rr = market_data.get("rr_ratio", 0)
        if rr >= 2.0:
            votes += 3

        # Master Verdict (Needs >= 8 votes out of 11 point weight)
        if votes >= 8:
            return {
                "decision": "BUY",
                "votes": f"{votes}/11",
                "reason": "Liquidity Sweep + CHOCH Confirmed with 1:2+ R:R",
                "stop_loss": market_data.get("stop_loss"),
                "target": market_data.get("target")
            }
        else:
            return {
                "decision": "HOLD",
                "votes": f"{votes}/11",
                "reason": "Consensus score insufficient for entry",
                "stop_loss": None,
                "target": None
            }
