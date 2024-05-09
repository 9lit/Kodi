from main.config import Config
import xml.etree.ElementTree as ET

class Kodi():

    def __init__(self, metadata_list) -> None:
        self.template_episode = Config.TEMPLATE_EPISODE
        self.metadata_tv = metadata_list['tv']
        self.metadata_season = metadata_list['season']
        self.metadata_episode:dict = metadata_list['episode']
        self.thumb_image_url = Config.THUMB_IMAGE_URL
        self.thumb_person_url = Config.THUMB_PERSON_URL
    
    def run(self):
        
        if self.metadata_episode:
            self.tmdb()
    
    def kodi_xml(self):
        self.tree = ET.parse(self.template_episode)
        self.root = self.tree.getroot()
    
    def pretty_xml(self, root=None, child=None, text=None, level=1):
        # 添加元素文本，并格式化（子元素缩进两个空格，并进行换行）
        
        newline = "\n"
        indet = "\t"
        
        if root:

            if level == 1:
                root.text = newline + indet*2
            else:
                root.text = newline + indet*level

            root.tail = newline + indet*(level-1)
            
        else:
            # 如果 text 有内容，则添加 text，并对此元素标签进行缩进 2 级并换行
            child.text = text
            child.tail = newline + indet*level

    def tmdb(self):
        # self.kodi_xml()

        def episodes(nfo):
            thumb = self.root.find('thumb')
            thumb_image_url = self.thumb_image_url + nfo['still_path']
            thumb.set('preview', thumb_image_url)

            uniqueid = self.root.find('uniqueid')
            uniqueid.set('type', 'tmdb')

            self.pretty_xml(child=self.root.find("title"), text=nfo['name'])
            self.pretty_xml(child=self.root.find("plot"), text=nfo['overview'])
            self.pretty_xml(child=self.root.find("runtime"), text=str(nfo['runtime']))
            self.pretty_xml(child=thumb, text=thumb_image_url)
            self.pretty_xml(child=uniqueid, text=str(nfo['id']))
            
            credits = self.root.find('credits')
            director = self.root.find('director')
            if nfo['crew']:
                for crew in nfo['crew']:
                    if crew['job'] == 'Director':
                        credits.text = crew['name']
                    elif crew['job'] == 'Writer':
                        director.text = crew['name']

            self.root.find('aired').text = nfo['air_date']

            actor = self.root.find('actor')
            self.pretty_xml(root=actor)
            mate_guest_stars = nfo['guest_stars']
            if mate_guest_stars:
                for index, mate_actor in enumerate(mate_guest_stars):
                    if len(mate_guest_stars) > 1:
                        new_actor = ET.SubElement(self.root, 'actor')
                        # self.pretty_xml(root=new_actor, level=2)
                        for child in actor:
                            ET.SubElement(new_actor, child.tag)

                    level = 1 if index + 1 == len(mate_guest_stars) else 2
                    self.pretty_xml(root=new_actor, level=level)
                    self.pretty_xml(child=new_actor.find('name'), text=mate_actor['name'], level=2)
                    self.pretty_xml(child=new_actor.find('role'), text=mate_actor['character'], level=2)
                    
                    thumb = new_actor.find('thumb')
                    text = "%s%s" % (self.thumb_person_url, mate_actor['profile_path'])
                    self.pretty_xml(child=thumb, text=text, level=2)
                    self.pretty_xml(child=new_actor.find('order'), text=str(mate_actor['order']), level=1)

            self.root.remove(actor)

        for metadata in self.metadata_episode.values():

            jpg = metadata["jpg"]
            outpath = metadata['outpath']


            for index, nfo in enumerate(metadata["nfo"]):
                new_outpath = outpath[index]
                new_jpg = jpg[index] if jpg else False


                self.kodi_xml()
                episodes(nfo)
                
                nfo_outpath = "%s.nfo" % new_outpath
                self.tree.write(nfo_outpath, xml_declaration=True, encoding='utf-8', method="xml")
                print("成功: %s" % nfo_outpath)

                if new_jpg:
                    jpg_outpath = "%s-thumb.jpg" % new_outpath
                    with open(jpg_outpath, 'wb') as f:
                        f.write(new_jpg.content)
                    print("成功: %s" % jpg_outpath)
                else:
                    print("失败: %s" % jpg_outpath)



    
