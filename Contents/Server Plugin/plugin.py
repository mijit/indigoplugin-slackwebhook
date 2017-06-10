#! /usr/bin/env python
# -*- coding: utf-8 -*-

import httplib, urllib, sys, os

from urlparse import urlparse

class Plugin(indigo.PluginBase):
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.debug = self.pluginPrefs.get("cfgDebug")

    def __del__(self):
        indigo.PluginBase.__del__(self)

    def dodebug(self, hdr, msg):
        self.debugLog("\n[%s]\n%s\n" % ( hdr, msg ))

    def notify(self, action):
        self.dodebug('action', action)

        payload = {}

        # these override any preferences set at plugin and webhook levels
        if action.props.get("cfgChannel"):
            payload["channel"] = action.props.get("cfgChannel").encode('ascii')

        if action.props.get("cfgIcon"):
            payload["icon_emoji"] = action.props.get("cfgIcon").encode('ascii')

        if action.props.get("cfgText"):
            payload["text"] = action.props.get("cfgText").encode('ascii')

        self.dodebug('payload', payload)

        if payload['text']:
            url = urlparse(self.pluginPrefs['cfgWebhookURL'])
            conn = httplib.HTTPSConnection(url.netloc)
            conn.request("POST",
                         url.path,
                         urllib.urlencode({ "payload": payload }),
                         {"Content-type": "application/x-www-form-urlencoded"}
                         )
            resp = conn.getresponse()
            self.debugLog("Slack returned %s %s: %s" % ( resp.status, resp.reason, resp.read()))
            conn.close

        else:
            self.errorLog("Empty message. Skipping Slack notification.")

