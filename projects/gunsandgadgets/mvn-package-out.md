> Canonical documentation: [TF-Minecraft/docs](https://github.com/TF-Minecraft/docs). [Source snapshot](https://github.com/TF-Minecraft/gunsandgadgets/blob/17a1894226083b927bc23f29d9649546e35d9eab/mvn-package-out.txt). Commands and plain-text code/config paths refer to the source repository unless stated otherwise.

[INFO] Scanning for projects...
[INFO] 
[INFO] -------------------< net.tfminecraft:gunsandgadgets >-------------------
[INFO] Building gunsandgadgets 1.0.3
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
[INFO] --- maven-resources-plugin:2.6:resources (default-resources) @ gunsandgadgets ---
[INFO] Using 'UTF-8' encoding to copy filtered resources.
[INFO] Copying 6 resources
[INFO] 
[INFO] --- maven-compiler-plugin:3.1:compile (default-compile) @ gunsandgadgets ---
[INFO] Changes detected - recompiling the module!
[INFO] Compiling 32 source files to D:\Documents\TFMC\Workspace\gunsandgadgets\target\classes
[INFO] -------------------------------------------------------------
[WARNING] COMPILATION WARNING : 
[INFO] -------------------------------------------------------------
[WARNING] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/manager/GunManager.java: Some input files use or override a deprecated API.
[WARNING] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/manager/GunManager.java: Recompile with -Xlint:deprecation for details.
[WARNING] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/manager/inventory/InventoryManager.java: D:\Documents\TFMC\Workspace\gunsandgadgets\src\main\java\net\tfminecraft\gunsandgadgets\manager\inventory\InventoryManager.java uses or overrides a deprecated API that is marked for removal.
[WARNING] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/manager/inventory/InventoryManager.java: Recompile with -Xlint:removal for details.
[INFO] 4 warnings 
[INFO] -------------------------------------------------------------
[INFO] -------------------------------------------------------------
[ERROR] COMPILATION ERROR : 
[INFO] -------------------------------------------------------------
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[3,40] cannot access net.tfminecraft.VehicleFramework.VehicleFramework
  bad class file: D:\Documents\TFMC\ReferenceLibs\vehicleframework-1.1.6.jar(/net/tfminecraft/VehicleFramework/VehicleFramework.class)
    class file has wrong version 65.0, should be 61.0
    Please remove or make sure it appears in the correct subdirectory of the classpath.
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[4,45] cannot access net.tfminecraft.VehicleFramework.Util.LightEffect
  bad class file: D:\Documents\TFMC\ReferenceLibs\vehicleframework-1.1.6.jar(/net/tfminecraft/VehicleFramework/Util/LightEffect.class)
    class file has wrong version 65.0, should be 61.0
    Please remove or make sure it appears in the correct subdirectory of the classpath.
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[5,49] cannot access net.tfminecraft.VehicleFramework.Vehicles.ActiveVehicle
  bad class file: D:\Documents\TFMC\ReferenceLibs\vehicleframework-1.1.6.jar(/net/tfminecraft/VehicleFramework/Vehicles/ActiveVehicle.class)
    class file has wrong version 65.0, should be 61.0
    Please remove or make sure it appears in the correct subdirectory of the classpath.
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[6,49] cannot access net.tfminecraft.VehicleFramework.Vehicles.Vehicle
  bad class file: D:\Documents\TFMC\ReferenceLibs\vehicleframework-1.1.6.jar(/net/tfminecraft/VehicleFramework/Vehicles/Vehicle.class)
    class file has wrong version 65.0, should be 61.0
    Please remove or make sure it appears in the correct subdirectory of the classpath.
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[69,18] cannot find symbol
  symbol:   class LightEffect
  location: class net.tfminecraft.gunsandgadgets.shooter.ProjectileShooter
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[73,26] cannot find symbol
  symbol: class LightEffect
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[77,34] cannot find symbol
  symbol: class LightEffect
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[176,46] cannot find symbol
  symbol:   variable EXPLOSION_HUGE
  location: class org.bukkit.Particle
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[179,14] cannot find symbol
  symbol:   class LightEffect
  location: class net.tfminecraft.gunsandgadgets.shooter.ProjectileShooter
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[183,22] cannot find symbol
  symbol: class LightEffect
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[187,30] cannot find symbol
  symbol: class LightEffect
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[392,13] cannot find symbol
  symbol:   class ActiveVehicle
  location: class net.tfminecraft.gunsandgadgets.shooter.ProjectileShooter
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[392,31] cannot find symbol
  symbol:   variable VehicleFramework
  location: class net.tfminecraft.gunsandgadgets.shooter.ProjectileShooter
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[417,37] cannot find symbol
  symbol:   variable BLOCK_DUST
  location: class org.bukkit.Particle
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[439,33] cannot find symbol
  symbol:   variable EXPLOSION_NORMAL
  location: class org.bukkit.Particle
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[519,29] cannot find symbol
  symbol:   variable FIREWORKS_SPARK
  location: class org.bukkit.Particle
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[529,29] cannot find symbol
  symbol:   variable SMOKE_NORMAL
  location: class org.bukkit.Particle
[INFO] 17 errors 
[INFO] -------------------------------------------------------------
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  6.122 s
[INFO] Finished at: 2026-08-08T22:31:06+02:00
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin:3.1:compile (default-compile) on project gunsandgadgets: Compilation failure: Compilation failure: 
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[3,40] cannot access net.tfminecraft.VehicleFramework.VehicleFramework
[ERROR]   bad class file: D:\Documents\TFMC\ReferenceLibs\vehicleframework-1.1.6.jar(/net/tfminecraft/VehicleFramework/VehicleFramework.class)
[ERROR]     class file has wrong version 65.0, should be 61.0
[ERROR]     Please remove or make sure it appears in the correct subdirectory of the classpath.
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[4,45] cannot access net.tfminecraft.VehicleFramework.Util.LightEffect
[ERROR]   bad class file: D:\Documents\TFMC\ReferenceLibs\vehicleframework-1.1.6.jar(/net/tfminecraft/VehicleFramework/Util/LightEffect.class)
[ERROR]     class file has wrong version 65.0, should be 61.0
[ERROR]     Please remove or make sure it appears in the correct subdirectory of the classpath.
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[5,49] cannot access net.tfminecraft.VehicleFramework.Vehicles.ActiveVehicle
[ERROR]   bad class file: D:\Documents\TFMC\ReferenceLibs\vehicleframework-1.1.6.jar(/net/tfminecraft/VehicleFramework/Vehicles/ActiveVehicle.class)
[ERROR]     class file has wrong version 65.0, should be 61.0
[ERROR]     Please remove or make sure it appears in the correct subdirectory of the classpath.
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[6,49] cannot access net.tfminecraft.VehicleFramework.Vehicles.Vehicle
[ERROR]   bad class file: D:\Documents\TFMC\ReferenceLibs\vehicleframework-1.1.6.jar(/net/tfminecraft/VehicleFramework/Vehicles/Vehicle.class)
[ERROR]     class file has wrong version 65.0, should be 61.0
[ERROR]     Please remove or make sure it appears in the correct subdirectory of the classpath.
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[69,18] cannot find symbol
[ERROR]   symbol:   class LightEffect
[ERROR]   location: class net.tfminecraft.gunsandgadgets.shooter.ProjectileShooter
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[73,26] cannot find symbol
[ERROR]   symbol: class LightEffect
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[77,34] cannot find symbol
[ERROR]   symbol: class LightEffect
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[176,46] cannot find symbol
[ERROR]   symbol:   variable EXPLOSION_HUGE
[ERROR]   location: class org.bukkit.Particle
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[179,14] cannot find symbol
[ERROR]   symbol:   class LightEffect
[ERROR]   location: class net.tfminecraft.gunsandgadgets.shooter.ProjectileShooter
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[183,22] cannot find symbol
[ERROR]   symbol: class LightEffect
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[187,30] cannot find symbol
[ERROR]   symbol: class LightEffect
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[392,13] cannot find symbol
[ERROR]   symbol:   class ActiveVehicle
[ERROR]   location: class net.tfminecraft.gunsandgadgets.shooter.ProjectileShooter
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[392,31] cannot find symbol
[ERROR]   symbol:   variable VehicleFramework
[ERROR]   location: class net.tfminecraft.gunsandgadgets.shooter.ProjectileShooter
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[417,37] cannot find symbol
[ERROR]   symbol:   variable BLOCK_DUST
[ERROR]   location: class org.bukkit.Particle
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[439,33] cannot find symbol
[ERROR]   symbol:   variable EXPLOSION_NORMAL
[ERROR]   location: class org.bukkit.Particle
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[519,29] cannot find symbol
[ERROR]   symbol:   variable FIREWORKS_SPARK
[ERROR]   location: class org.bukkit.Particle
[ERROR] /D:/Documents/TFMC/Workspace/gunsandgadgets/src/main/java/net/tfminecraft/gunsandgadgets/shooter/ProjectileShooter.java:[529,29] cannot find symbol
[ERROR]   symbol:   variable SMOKE_NORMAL
[ERROR]   location: class org.bukkit.Particle
[ERROR] -> [Help 1]
[ERROR] 
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR] 
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoFailureException
