from IPython.display import display
from cast_common.highlight import Highlight
from pandas import DataFrame,Series,json_normalize
from cast_common.logger import Logger, INFO,DEBUG
from cast_common.powerpoint import PowerPoint

class GreenIt(Highlight):

    def report(self,app:str,prs:PowerPoint) -> bool:
        status = True
        try:
            index = hl.get_green_indexes(app)
            for idx,val in index.items():
                if idx == 'greenOccurrences':
                    val = int(val)
                tag = f'{{app1_{idx}}}'
                prs.replace_text(tag,val)

            detail = hl.get_green_detail(app)

            agr = detail[['Technology','Occurrences']].groupby('Technology').aggregate('sum').reindex()
            prs.update_chart('app1GreenTechPieChart',agr)
            agr.sort_values('Occurrences',ascending=False,inplace=True)
            prs.replace_text('{app1_green_top_lang}',agr.index[0])
            prs.replace_text('{app1_green_top_lang_count}',int(agr.iloc[0,0]))

            agr = detail[['Name','Occurrences']].groupby('Name').aggregate('sum').reindex()
            agr.sort_values('Occurrences',ascending=False,inplace=True)
            prs.replace_text('{app1_green_top_rule1}',agr.index[0])
            prs.replace_text('{app1_green_top_rule2}',agr.index[1])

            detail.sort_values(by=['Occurrences'],ascending=False,inplace=True)
            detail['Contribution'] = detail['Contribution'].apply(lambda x: '{0:.2f}%'.format(x).rjust(10))
            detail['Occurrences'] = detail['Occurrences'].apply(lambda x: '{0:,.0f}'.format(x).rjust(10))
            hl.create_excel(app,detail)

            #detail = detail.astype({'Contribution':'string'})
            #detail['Contribution'] = detail['Contribution'].str.ljust(20)
            prs.update_table('app1GreenDetailTable',detail,include_index=False,max_rows=8)


            pass      

        except Exception as ex:
            self.log.error(ex)
            status = False

        return status

    def get_green_indexes(self,app_name:str) -> Series:
        self.log.info(f'Retrieving green it index data for: {app_name}')
        try:
            df = json_normalize(self._get_metrics(app_name)['greenDetail'],['greenIndexDetails'],meta=['technology','greenIndexScan']).dropna(axis='columns')
            df = df[['greenIndexScan','greenOccurrences','greenEffort']]
            df = df.aggregate(['sum','average'])

            if self.log.is_debug:
                self.log.debug('aggragation')
                display(df)

            rslt = Series()
            rslt.loc['greenEffort']=round(df.loc['sum','greenEffort']/60/8,1)
            rslt.loc['greenOccurrences']=round(df.loc['sum','greenOccurrences'],0)
            rslt.loc['greenIndexScan']=round(df.loc['average','greenIndexScan']*100,1)

            if self.log.is_debug:
                self.log.debug('final')
                display(rslt)

            return rslt
        except KeyError as ke:
            self.warning(f'{app_name} has no Green IT Data')
            return None

    def get_green_detail(self,app_name:str)->DataFrame:
        """Highlight green it data

        Args:
            app_name (str): name of the application

        Returns:
            DataFrame: flattened version of the Highlight green it data
        """
        self.log.info(f'Retrieving green it detail data for: {app_name}')
        try:
            df = json_normalize(self._get_metrics(app_name)['greenDetail'],['greenIndexDetails'],meta=['technology','greenIndexScan']).dropna(axis='columns')
            df.drop(columns=['greenRequirement.id','greenRequirement.hrefDoc','triggered','greenRequirement.ruleType','greenIndexScan'],inplace=True)
            df.rename(columns={'contributionScore':'Contribution',
                               'greenOccurrences':'Occurrences',
                               'greenRequirement.display':'Name',
                               'greenEffort':'Effort',
                               'technology':'Technology'},
                               inplace=True)
            df['Effort']=df['Effort'].div(60).div(8).round(2)
            df['Contribution']=df['Contribution'].round(2)
            return df[['Name','Technology','Contribution','Occurrences','Effort']]
        except KeyError as ke:
            self.warning(f'{app_name} has no Green IT Data')
            return None

    def create_excel(self,app_name:str,data:DataFrame):
        file_name = abspath(f'E:/work/Decks/test/greenIt-Reporting-{app_name}.xlsx')
        writer = ExcelWriter(file_name, engine='xlsxwriter')
        format_table(writer,data,'Detail',width=[75,25,15,15,15],total_line=True)
        writer.close()

from os.path import abspath
from cast_common.util import format_table
from pandas import ExcelWriter

ppt = PowerPoint(r'E:\work\Decks\highlight-test.pptx',r'E:\work\Decks\test\highlight.pptx')

app = 'Sol'
                            
hl = GreenIt('n.kaplan+VistaSOL@castsoftware.com','vadKpBFAZ8KIKb2f2y',hl_instance=22642,hl_base_url='https://rpa.casthighlight.com',log_level=DEBUG)
app_cnt = len(hl.app_list)
hl.report(app,ppt)
ppt.save()



