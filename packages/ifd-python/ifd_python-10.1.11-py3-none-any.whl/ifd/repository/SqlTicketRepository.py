from .abstract import AbsSqlRepository
import pandas as pd 
from ..entities import Ticket

class SqlTicketRepository(AbsSqlRepository):
    
    def getAll(self):
        if not self.is_open:
            self._connectToDatabase()
            
        df = pd.read_sql_query(
            """
            EXEC PROC_SELECT_IRRIS_TICKET_AUTOMATIC_ITA
            """, 
            self.connection
        )
        self.close()
        return self._dataframe_to_list_of_ticket(df)
    
    def updateStatut(self, ticket, statut, message):
        if not self.is_open:
            self._connectToDatabase()
        
        ticket.ita_ticket_request = ticket.ita_ticket_request.replace("'", "''")
        
        cur = self.connection.cursor()
        req = f"""
            UPDATE [Infradeep].[dbo].[T_D_IRRIS_TICKET_AUTOMATIC_ITA]
            SET ITA_VALIDATION_STATUT = '{statut}', ITA_TICKET_RESPONSE = '{message}', ITA_DATE_ACTION_TICKET = GETDATE()
            WHERE ITA_ID = {ticket.ita_id}
            """
        cur.execute_non_query(req)
        cur.close()
        
    def insertLog(self, ticket, sendRoute, response, expediteur):
        if not self.is_open:
            self._connectToDatabase()
            
        cur = self.connection.cursor()
        
        ticket.ita_ticket_request = ticket.ita_ticket_request.replace("'", "''")
        response = response.replace("'", "''")

        req = f"""
            INSERT INTO T_L_LOGS_IRRIS_LIR (IMG_ID ,LIR_ROUTE ,LIR_REQUEST ,LIR_RESPONSE ,LIR_EXPEDITEUR)
            VALUES(
            {ticket.img_id},
            '{sendRoute}',
            '{ticket.ita_ticket_request}',
            '{response}',
            '{expediteur}'
            )
            """
        cur.execute_non_query(req)
        cur.close()
                
        
    def _dataframe_to_list_of_ticket(self, df):
        return [Ticket(**kwargs) for kwargs in df.to_dict(orient='records')]