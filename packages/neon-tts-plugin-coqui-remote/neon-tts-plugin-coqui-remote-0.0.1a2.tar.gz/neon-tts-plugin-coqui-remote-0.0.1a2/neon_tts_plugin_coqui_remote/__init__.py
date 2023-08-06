# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import requests

from urllib.parse import quote
from typing import Optional
from ovos_plugin_manager.templates.tts import RemoteTTS, TTSValidator

from .configs import languages


class CoquiRemoteTTS(RemoteTTS):
    # TODO: Update to query remote API
    langs = languages

    def __init__(self, lang: str = "en", config: dict = None, api_path: str = '/synthesize'):
        default_url = 'https://coqui.2021.us'
        config = config or dict()
        super(CoquiRemoteTTS, self).__init__(lang, config, default_url, api_path, CoquiRemoteTTSValidator(self))

    def get_tts(self, sentence: str, output_file: str,
                speaker: Optional[dict] = None, lang: Optional[str] = None) -> (str, Optional[str]):
        """
        Get Synthesized audio
        Args:
            sentence: string to synthesize
            output_file: path to output audio file
            speaker: optional dict speaker data
            lang: optional lang override
        Returns:
            tuple wav_file, optional phonemes
        """
        speaker = speaker or dict()
        lang = lang or speaker.get('language') or self.lang

        resp = requests.get(f'{self.url}{self.api_path}/{quote(sentence)}', params={'lang': lang})
        if resp.status_code != 200:
            return None
        with open(output_file, 'wb') as f:
            f.write(resp.content)
        return output_file, None

    @property
    def available_languages(self):
        return set(self.langs.keys())


class CoquiRemoteTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(CoquiRemoteTTSValidator, self).__init__(tts)

    def validate_lang(self):
        if self.tts.lang.split('-')[0] not in CoquiRemoteTTS.langs:
            raise KeyError(f"Language isn't supported: {self.tts.lang}")

    def validate_dependencies(self):
        # TODO: Optionally check dependencies or raise
        pass

    def validate_connection(self):
        # TODO: Optionally check connection to remote service or raise
        pass

    def get_tts_class(self):
        return CoquiRemoteTTS
