import requests,json
class check:
	def Telegram(self,user):
		response=requests.get(f"https://t.me/{user}")
		if response.text.find('If you have <strong>Telegram</strong>, you can contact <a class="tgme_username_link"')>=0:
			status = "available"
		else:
			status = "not available"
		return status			
		pass
	def Auction(self,user):
		response=requests.get(f"https://saiko-team.fun/fragment/?user={user}")
		if response.text.find('1')>=0:
			status = "auction"
		else:
			status = "not auction"
		return status			
		pass
