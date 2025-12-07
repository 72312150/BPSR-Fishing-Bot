import time

from ..bot_state import BotState
from ..state_type import StateType


class CheckingRodState(BotState):

    def handle(self, screen):
        self.bot.log("[CHECKING_ROD] Checking rod...")

        time.sleep(1)

        if self.detector.find(screen, "broken_rod"):
            self.bot.log("[CHECKING_ROD] ⚠️  Broken rod! Replacing...")
            self.bot.stats.increment('rod_breaks')
            time.sleep(1)

            # Open inventory
            self.controller.press_key('m')
            time.sleep(1.5)  # Wait for inventory to open
            
            # Capture a fresh screen after opening inventory
            screen = self.detector.capture_screen()
            
            # Find the new_rod template
            pos = self.detector.find(screen, "new_rod", debug=self.bot.debug_mode)
            
            if pos is None:
                self.bot.log("[CHECKING_ROD] ❌ Could not find new_rod template!")
                return StateType.CHECKING_ROD  # Stay in this state to retry
            
            self.bot.log(f"[CHECKING_ROD] ✅ Found new_rod at {pos}")

            # Click on the new rod (inventory closes automatically)
            self.controller.move_to(pos[0], pos[1])
            time.sleep(0.5)
            self.controller.move_to(pos[0], pos[1])
            time.sleep(0.5)
            self.controller.click('left')
            time.sleep(1)

            self.bot.log("[CHECKING_ROD] ✅ Rod replaced")
        else:
            time.sleep(1)
            self.bot.log("[CHECKING_ROD] ✅ Rod OK")

        return StateType.CASTING_BAIT
