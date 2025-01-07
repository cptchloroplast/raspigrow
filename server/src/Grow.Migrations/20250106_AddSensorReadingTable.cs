using FluentMigrator;
namespace Grow.Migrations;
[Migration(20250106)]
public class AddSensorReadingTable : Migration
{
    public override void Up()
    {
        Create.Table("SensorReading")
            .WithColumn("Timestamp").AsDateTime().NotNullable().Indexed()
            .WithColumn("Temperature").AsFloat().NotNullable()
            .WithColumn("Humidity").AsInt32().NotNullable()
            .WithColumn("SystemKey").AsGuid().PrimaryKey().NotNullable().Indexed()
            .WithColumn("SystemCreatedDate").AsString().NotNullable()
            .WithColumn("SystemModifiedDate").AsString().NotNullable();
    }
    public override void Down()
    {
        Delete.Table("SensorReading");
    }
}