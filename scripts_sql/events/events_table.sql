CREATE TABLE Events_Stats (
    Time VARCHAR2(100),
    Posicao_Inicial NUMBER,
    Posicao_Final NUMBER,
    Evento VARCHAR2(255),
    Evento_URL VARCHAR2(255),
    Wins NUMBER,
    Draws NUMBER,
    Losses NUMBER,
    Maps_Played NUMBER,
    Total_Kills NUMBER,
    Total_Deaths NUMBER,
    Rounds_Played NUMBER,
    KD_Ratio FLOAT
);
DROP TABLE Esports_Stats;




ALTER SESSION SET NLS_NUMERIC_CHARACTERS = '. ,';