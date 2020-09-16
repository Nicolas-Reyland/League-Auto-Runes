import tkinter as tk
from tkinter.messagebox import showerror

class CustomTkWidget:

	def __init__(self, frame, info, function, popup_onerror=True, TkWidget=tk.Button, use_callback=True, **kwargs):

		self.frame = frame
		self.info = info
		self.function = function

		self.popup_onerror = popup_onerror
		self.exception_hist = []
		self.use_callback = use_callback
		self.kwargs = kwargs

		self.TkWidget = TkWidget

		if self.use_callback: self.widget = self.TkWidget(self.frame, command=self.call, **kwargs)
		else: self.widget = self.TkWidget(self.frame, **kwargs)
		self.callback_count = 0

	def call(self):
		if self.popup_onerror:
			try: self.function(self.info)
			except Exception as e: self.exception_hist.append([self.info, e])
		else:
			self.function(self.info)
		self.callback_count += 1

	def destroy(self):
		self.widget.destroy()

