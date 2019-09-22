import tkinter
from tkinter import ttk
from tkinter import filedialog
import pytube
import codecs
import subprocess
import requests
import time

#用於判斷使用者下載需求的變數開關
#確認次數、影片格式、畫質優劣
global ConfirmTimes, Format_Choice, Picture_Quality, Previous, Later, Flag1, Flag2, filename
global YT_Info

#定義檢查按鈕的函式
def Get_Info():
	global ConfirmTimes, Format_Choice, Picture_Quality, Previous, Later, SaveRoute, Flag1, Flag2, filename
	global YT_Info
	try:
		if CheckButton["text"] == "Check#":
			#影片搜尋
			ConfirmTimes = 0
			Format_Choice = -1
			Picture_Quality = -1
			Flag1 = -1
			Flag2 = -1
			YT_Info = pytube.YouTube(Var_UrlInput.get())
			Previous = Var_UrlInput.get()
			Var_Title.set(YT_Info.title)
			ConfirmTimes += 1
			Var_Choice.set("請選擇要下載的格式：\n1. MP3音訊檔\n2. MP4視訊檔")
		elif CheckButton["text"] == "Download#":
			Later = Var_UrlInput.get()
			if Previous != Later:
				Var_Title.set("網址有更動，請重新操作！\n請輸入你想下載的YouTube影音網址：")
				Var_UrlInput.set("")
				Var_Choice.set("")
				Var_ChoiceInput.set("")
				CheckButton["text"] = "Check#"
			else:
				SaveRoute = None
				if Var_SaveAddress.get() != "None":
					SaveRoute = Var_SaveAddress.get()
				#YT_Info.register_on_complete_callback(Complete_DownLoad)
				#YT_Info.register_on_progress_callback(DownLoading)
				filename = ""
				for word in YT_Info.title:
					if word == "<" or word == ">" or word == "?" or word == ":" or word == '"' or word == "/" or word == "\\" or word == "*" or word == "|" or word == ";":
						TempName = "_"
						filename += TempName
					else:
						filename += word
				#影片下載
				if Format_Choice == 2 and Picture_Quality == 1:
					Stream = YT_Info.streams.filter(mime_type="video/webm", adaptive=True).first()
					Stream.download(filename="Temp_Stream")
				elif Format_Choice == 2 and Picture_Quality == 2:
					Stream = YT_Info.streams.filter(file_extension="mp4", progressive=True).first()
					Stream.download(output_path=SaveRoute, filename=filename)
				#音訊下載
				if Format_Choice == 1 or (Format_Choice == 2 and Picture_Quality == 1):
					Stream = YT_Info.streams.filter(mime_type="audio/mp4").first()
					Stream.download(filename="Temp_Audio")
				
				#合併視訊跟音檔
				Command = "OuO"
				if SaveRoute == None:
					if Format_Choice == 2 and Picture_Quality == 1:
						Command = 'ffmpeg -i Temp_Stream.webm -i Temp_Audio.mp4 "{}.mp4"'.format(filename)
					elif Format_Choice == 1:
						Command = 'ffmpeg -i Temp_Audio.mp4 "{}.mp3"'.format(filename)
					#elif Format_Choice == 2 and Picture_Quality == 2:
						#Command = "move Temp_Stream.mp4 {}.mp4".format(filename)
				else:
					if Format_Choice == 2 and Picture_Quality == 1:
						Command = 'ffmpeg -i Temp_Stream.webm -i Temp_Audio.mp4 "{}\\{}.mp4"'.format(SaveRoute, YT_Info.title)
					elif Format_Choice == 1:
						Command = 'ffmpeg -i Temp_Audio.mp4 "{}\\{}.mp3"'.format(SaveRoute, filename)
					#elif Format_Choice == 2 and Picture_Quality == 2:
						#Command = "move Temp_Stream.mp4 {}\\{}.mp4".format(SaveRoute, filename)
				if Command != "OuO":
					subprocess.call(args=Command, shell=True)

				ConfirmTimes = 2

				#字幕下載
				Caption = YT_Info.captions.get_by_language_code('zh-TW')
				if Caption == None:
					ConfirmTimes = 0
					Var_Choice.set("下載完成！\n此影片沒有中文字幕#")
					Var_UrlInput.set("")
					CheckButton["text"] = "Check#"
				else:
					Var_Choice.set("如果需要中文字幕，請輸入1.\n若不需要字幕，請輸入0.")
					ConfirmTimes += 1

	except Exception as Error:
		print(Error)

#定義尋訪按鈕的函式
def Save_As():
	Location = filedialog.askdirectory(initialdir=Var_SaveAddress.get(), title="選擇儲存位置：")
	Var_SaveAddress.set(Location)

#定義下載中與下載完成的函式
#def Complete_DownLoad(stream, file_handle):
	#print("Download Finished.")
#def DownLoading(stream, chunk, file_handle, bytes_remaining):
	#global Bar
	#Finished = Stream[Stream_Choice-1].filesize-bytes_remaining
	#All = Stream[Stream_Choice-1].filesize
	#if Finished/All*100 >= Bar*100:
		#print("\r{}\n{:.0f}% {}/{}".format("▋"*(int(Finished/All*100//10)), Bar*100, Finished, All))
		#Bar += 0.1

#定義確認按鈕的函式
def Confirm():
	global ConfirmTimes, Format_Choice, Picture_Quality, Flag1, Flag2, filename
	if ConfirmTimes == 0:
		Var_Choice.set("未輸入影音網址，請重新操作。")
	elif ConfirmTimes == 1:
		if Var_ChoiceInput.get() == "1" and Flag1 != 1:
			Format_Choice = 1
			Var_Choice.set("已確認下載格式：MP3檔\n若要重新選擇請輸入0.")
			Flag1 = 1
			Flag2 = -1
			CheckButton["text"] = "Download#"
		elif Var_ChoiceInput.get() == "2" and Flag1 != 1:
			Var_Choice.set("請選擇要下載的影片品質：\n1. 高畫質\n2. 低畫質")
			Var_ChoiceInput.set("")
			ConfirmTimes += 1
			Format_Choice = 2
		elif Var_ChoiceInput.get() == "0" and Flag1 != -1:
			Var_Choice.set("要下載的格式：\n1. MP3音訊檔\n2. MP4視訊檔")
			Format_Choice = -1
			Picture_Quality = -1
			Flag1 = -1
			Flag2 = -1
			CheckButton["text"] = "Check#"
		else:
			if CheckButton["text"] == "Download#":
				Var_Choice.set("輸入錯誤，請重新嘗試。\n已確認下載格式：MP3檔\n若要重新選擇請輸入0.")
			else:
				Var_Choice.set("輸入錯誤，請重新嘗試。\n請選擇要下載的格式：\n1. MP3音訊檔\n2. MP4視訊檔")

	elif ConfirmTimes == 2:
		if Var_ChoiceInput.get() == "1" and Flag2 != 1:
			Picture_Quality = 1
			Var_Choice.set("已確認下載格式：高畫質MP4檔\n若要重新選擇請輸入0.")
			Flag2 = 1
			CheckButton["text"] = "Download#"
		elif Var_ChoiceInput.get() == "2" and Flag2 != 1:
			Picture_Quality = 2
			Var_Choice.set("已確認下載格式：低畫質MP4檔\n若要重新選擇請輸入0.")
			Flag2 = 1
			CheckButton["text"] = "Download#"
		elif Var_ChoiceInput.get() == "0" and Flag2 != -1:
			ConfirmTimes -= 1
			Var_Choice.set("要下載的格式：\n1. MP3音訊檔\n2. MP4視訊檔")
			Format_Choice = -1
			Picture_Quality = -1
			Flag1 = -1
			Flag2 = -1
			CheckButton["text"] = "Check#"
		else:
			if CheckButton["text"] == "Download#":
				if Picture_Quality == 1:
					Var_Choice.set("輸入錯誤，請重新嘗試。\n已確認下載格式：高畫質MP4檔\n若要重新選擇請輸入0.")
				elif Picture_Quality == 2:
					Var_Choice.set("輸入錯誤，請重新嘗試。\n已確認下載格式：低畫質MP4檔\n若要重新選擇請輸入0.")
			else:
				Var_Choice.set("輸入錯誤，請重新嘗試。\n請選擇要下載的影片品質：\n1. 高畫質\n2. 低畫質")

	elif ConfirmTimes == 3:
		if Var_ChoiceInput.get() == "1":
			Caption = YT_Info.captions.get_by_language_code('zh-TW')
			if SaveRoute == None:
				SubTitle = codecs.open("{}.srt".format(filename), mode="w+", encoding="UTF-8")
			else:
				SubTitle = codecs.open(SaveRoute+"\\{}.srt".format(filename), mode="w+", encoding="UTF-8")
			SubTitle.write(Caption.generate_srt_captions())
			SubTitle.close()
			# Var_Choice.set("字幕下載完成！~\n可以繼續使用了#")
			Var_Title.set("請輸入你要下載的YouTube影音：")
			Var_Choice.set("")
			ConfirmTimes = 0
			Format_Choice = -1
			Picture_Quality = -1
			Var_UrlInput.set("")
			CheckButton["text"] = "Check#"
		elif Var_ChoiceInput.get() == "0":
			# Var_Choice.set("不下載字幕#\n可以繼續使用了#")
			Var_Title.set("請輸入你要下載的YouTube影音：")
			Var_Choice.set("")
			ConfirmTimes = 0
			Format_Choice = -1
			Picture_Quality = -1
			Var_UrlInput.set("")
			CheckButton["text"] = "Check#"
		else:
			Var_Choice.set("輸入錯誤，請重新嘗試。\n如果需要中文字幕，請輸入1.\n若不需要字幕，請輸入0.")
	Var_ChoiceInput.set("")
	Var_DownloadCheck.set("")
	print(ConfirmTimes, Format_Choice, Picture_Quality)

#設定視窗參數
width=400
height=400
Gui = tkinter.Tk()
Gui.title("YouTube下載器OAO#")
Gui.resizable(0, 0)
Gui.geometry(str(width)+"x"+str(height))
ConfirmTimes = 0
Format_Choice = -1
Picture_Quality = -1
Flag1 = -1
Flag2 = -1

#建立動態字串
Var_UrlInput = tkinter.StringVar()
Var_Title = tkinter.StringVar()
Var_Title.set("請輸入你想下載的YouTube影音網址：")
Var_SaveAddress = tkinter.StringVar()
Var_SaveAddress.set(None)
Var_ChoiceInput = tkinter.StringVar()
Var_Choice = tkinter.StringVar()
Var_DownloadCheck = tkinter.StringVar()

#建立視窗元件
VideoUrlEntry = ttk.Entry(Gui, width=30, textvariable=Var_UrlInput)
CheckButton = ttk.Button(Gui, width=10, text="Check#", command=Get_Info)
Title = ttk.Label(Gui, width=30, textvariable=Var_Title)
AddressButton = ttk.Button(Gui, width=3, text="...", command=Save_As)
ChoiceEntry = ttk.Entry(Gui, width=10, textvariable=Var_ChoiceInput)
ChoiceButton = ttk.Button(Gui, width=5, text="確認", command=Confirm)
ChoiceMonitor = ttk.Label(Gui, width=30, textvariable=Var_Choice)

#調整元件位置
VideoUrlEntry.place(x=10, y=15)
CheckButton.place(x=230, y=13)
Title.place(x=10, y=40)
AddressButton.place(x=310, y=13)
ChoiceEntry.place(x=10, y=200)
ChoiceButton.place(x=95, y=198)
ChoiceMonitor.place(x=10, y=230)

Gui.mainloop()