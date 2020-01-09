# -*- coding: utf-8 -*-

from selenium import webdriver
from collections import OrderedDict
from time import sleep

class Scrapper():
    
    __slots__ = ('__personal_path', '__geckodriver', '__main_url', 'decklists', 'metas', '__card_types', 'params', 
                 'driver', 
                 '__titles', '__dates', '__tournament_links',
                 '__names', '__scores', '__raw_decklists',
                 )    
    
    def __init__(self, personal_path, params = None):
        super(Scrapper, self).__init__()
        self.__personal_path = personal_path
        self.__geckodriver = self.__personal_path + 'geckodriver-v0.26.0-win64/geckodriver.exe'
        self.__main_url = 'https://magic.wizards.com/en/content/deck-lists-magic-online-products-game-info'
        self.decklists = list()
        self.metas = list()
        self.__card_types = ['Creature', 'Sorcery', 'Instant', 'Artifact', 'Enchantement',
                             'Planeswalker', 'Tribal', 'Land']
        self.params = params
        if self.params is None:
            self.params = OrderedDict({'from_date' : '01/04/2020', 
                                       'to_date' : '01/07/2020',
                                       'research': 'Pioneer'})
        elif type(self.params) != type(OrderedDict()):
            self.params = OrderedDict(self.params)
        
    def connectBrowser(self):
        self.driver = webdriver.Firefox(executable_path = self.__geckodriver)
        
    def connectURL(self, url):
        self.driver.get(url)
        try:
            sleep(.5)
            class_button_agree = self.driver.find_element_by_class_name('button.agree')
            class_button_agree.click()
            sleep(.5)
        except:
            pass
        
    def filterLinks(self):
        id_datepickerFrom = self.driver.find_element_by_id('datepickerFrom')
        id_datepickerFrom.send_keys(self.params['from_date'])
        id_datepickerTo = self.driver.find_element_by_id('datepickerTo')
        id_datepickerTo.send_keys(self.params['to_date'])
        class_form_text = self.driver.find_element_by_class_name('form-text')
        class_form_text.send_keys(self.params['research'])
        class_custom_search_submit = self.driver.find_element_by_class_name('item-wrap.search-btn.see-more-article-listing-section-search')
        class_custom_search_submit = class_custom_search_submit.find_element_by_id('custom-search-submit')
        self.driver.execute_script("arguments[0].click();", class_custom_search_submit)
        sleep(.5)
        
    def scrollerLinks(self):
        class_see_more_archives = self.driver.find_element_by_class_name('see-more.see-more-article-listing-section')
        __next = True
        while __next:
            try:
                class_see_more_archives.click()
                class_see_more_archives = self.driver.find_element_by_class_name('see-more.see-more-article-listing-section')
                sleep(.5)
            except:
                __next = False
        
    def gatherLinks(self):
        self.__titles = [ element.text for element in self.driver.find_elements_by_class_name('title') ]
        self.__dates = [ element.text for element in self.driver.find_elements_by_class_name('date') ]
        elems = self.driver.find_elements_by_css_selector('div.article-item-extended >a')
        self.__tournament_links = [ element.get_attribute("href") for element in elems ]
    
    def gatherDeckLists(self):
        class_deck_meta = [ element.text.split('\n')[0] for element in self.driver.find_elements_by_class_name('deck-meta') ]
        self.__names = [ ' '.join(element_text.split(' ')[:-1]) for element_text in class_deck_meta ]
        self.__scores = [ ( element_text.split(' ')[-1] if len(element_text.split(' '))>1 else None ) for element_text in class_deck_meta]
        self.__raw_decklists = [ element.text for element in self.driver.find_elements_by_class_name('deck-list-text') ]
        
    def readDeckList(self, __raw_decklists):
        return [ self.textDeckList(decklist) for decklist in __raw_decklists ]
        #return [ self.parserDeckList(decklist) for decklist in __raw_decklists ]
    
    def metaDeckList(self, __names, __scores):
        return [ [__names[i], __scores[i]] for i in range(len(__names)) ]
    
    def parserDeckList(self, str_decklist):
        dict_decklist = OrderedDict()
        dict_decklist['Types'] = OrderedDict(dict([(card_type, 0) for card_type in self.__card_types]))
        dict_decklist['MD'] = OrderedDict()
        dict_decklist['SB'] = OrderedDict()
        
        str_decklist = str_decklist.split('Sideboard')
        str_md = str_decklist[0].split('\n')
        str_sb = str_decklist[1].split('\n')
        
        dict_decklist['SB']['Count'] = str_sb[0].split('(')[-1].split(')')[0]
        try:
            dict_decklist['SB']['Count'] = int(dict_decklist['SB']['Count'])
            dict_decklist['SB']['SB'] = str_sb[1]
        except:
            dict_decklist['SB']['Count'] = None
        
        __next = True
        for row in str_md:
            if __next:
                row_split = (' '.join(row.split(' ')[1:]), row.split(' ')[0])
                if any([card_type in row for card_type in self.__card_types]):
                    try:
                        dict_decklist['Types'][row_split[1]] = row_split[0].split('(')[-1].split(')')[0]
                    except:
                        dict_decklist['Types'][row_split[1]] = None
                elif 'Cards' not in row:
                    try:
                        dict_decklist['MD'][row_split[0]] = int(row_split[1])
                    except:
                        dict_decklist['MD'][row_split[1]] = None
                else:
                    __next = False
            else:
                pass        
        
        return dict_decklist
    
    def textDeckList(self, str_decklist):
        return str_decklist.split('\n')
        
    def writeFileText(self, decklists, meta, filename = None):
        if '/' in self.params['from_date']:
            from_date = '_'.join(self.params['from_date'].split('/'))
        else:
            from_date = self.params['from_date']
        if '/' in self.params['to_date']:
            to_date = '_'.join(self.params['to_date'].split('/'))
        else:
            to_date = self.params['to_date']
        if filename is None:
            filename = 'decklists_' + self.params['research'] + '_' + from_date + '_' + to_date
        with open(self.__personal_path+'data/'+filename+'.txt', 'w') as open_file:
            open_file.write(self.params['research'] + ' ' + self.params['from_date'] + ' ' + self.params['to_date'])
            for i in range(5):
                open_file.write('\n')
            for i, title in enumerate(self.__titles):
                open_file.write('CATEGORY')
                open_file.write(title + '\n')
                open_file.write(self.__dates[i] + '\n')
                open_file.write('\n')
                for j, decklist in enumerate(decklists[i]):
                    open_file.write('DECKLIST')
                    open_file.write(meta[i][j][0] + ' ')
                    open_file.write(meta[i][j][1] + '\n')
                    for row in decklist:
                        open_file.write(row+'\n')
                    open_file.write('\n')
                for k in range(3):
                    open_file.write('\n')
    
    def writeFileCsv(self, decklists):
        pass
    
    def run(self):
        self.connectBrowser()
        self.connectURL(self.__main_url)
        self.filterLinks()
        self.scrollerLinks()
        self.gatherLinks()
        
        for tournament_link in self.__tournament_links:
            self.connectURL(tournament_link)
            self.gatherDeckLists()
            #get names & scores too
            self.decklists += [self.readDeckList(self.__raw_decklists)]
            self.metas += [self.metaDeckList(self.__names, self.__scores)]
            sleep(.5)
        self.stop()
    
    def stop(self):
        self.driver.quit()
        
    def __str_cleaner(self, text):
        pass
    
if __name__ == '__main__':
    scrapper = Scrapper('C:/Users/julie/mtgodecklists/',
            {'from_date' : '01/05/2020', 'to_date' : '01/06/2020', 'research': 'Pioneer'})
    scrapper.run()
    scrapper.stop()
    scrapper.writeFileText(scrapper.decklists, scrapper.metas)

#test / in progress stuff
